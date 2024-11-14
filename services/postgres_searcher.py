"""
PostgresSearcher is a class that searches for items in a PostgreSQL 
database using a hybrid search strategy.
"""

# pylint:disable=import-error,missing-function-docstring,missing-class-docstring,unsupported-binary-operation
from typing import Union
from sqlalchemy import Float, Integer, column, select, text
from sqlalchemy.orm import joinedload

from services.embedding import Embedding
from models.database import get_db_session

embedding_util = Embedding()


class PostgresSearcher:

    embed_model: str = "text-embedding-3-small"

    def __init__(
        self,
        db_model,
        embed_dimensions: Union[int, None] = 1536,
    ):
        self.db_model = db_model
        self.embed_dimensions = embed_dimensions

    def build_filter_clause(self, filters) -> tuple[str, str]:
        if filters is None:
            return "", ""
        filter_clauses = []
        for filter in filters:
            if isinstance(filter["value"], str):
                filter["value"] = f"'{filter['value']}'"
            elif isinstance(filter["value"], list):
                comparison_operator = filter["comparison_operator"]
                if comparison_operator != "&&":
                    filter["value"] = (
                        "(" + ",".join([f"'{v}'" for v in filter["value"]]) + ")"
                    )
                else:
                    _vals = [f'"{v}"' for v in filter["value"]]
                    filter["value"] = "'{" + ",".join(_vals) + "}'"
            filter_clauses.append(
                f"{filter['column']} {filter['comparison_operator']} {filter['value']}"
            )
        filter_clause = " AND ".join(filter_clauses)
        if len(filter_clause) > 0:
            return f"WHERE {filter_clause}", f"AND {filter_clause}"
        return "", ""

    def search(
        self,
        query_text: Union[str, None],
        query_vector: Union[list[float], list],
        top: int = 5,
        filters: Union[list[dict], None] = None,
    ):
        filter_clause_where, filter_clause_and = self.build_filter_clause(filters)

        table_name = self.db_model.__tablename__
        embedding_field_name = self.db_model.get_embedding_field()
        search_text_field_name = self.db_model.get_text_search_field()

        vector_query = f"""
            SELECT id, RANK () OVER (ORDER BY {embedding_field_name} <=> :embedding) AS rank
                FROM "{table_name}"
                {filter_clause_where}
                ORDER BY {embedding_field_name} <=> :embedding
                LIMIT 20
            """

        fulltext_query = f"""
            SELECT id, RANK () OVER (ORDER BY ts_rank_cd(to_tsvector('english', {search_text_field_name}), query) DESC)
                FROM "{table_name}", plainto_tsquery('english', :query) query
                WHERE to_tsvector('english', {search_text_field_name}) @@ query {filter_clause_and}
                ORDER BY ts_rank_cd(to_tsvector('english', {search_text_field_name}), query) DESC
                LIMIT 20
            """

        hybrid_query = f"""
        WITH vector_search AS (
            {vector_query}
        ),
        fulltext_search AS (
            {fulltext_query}
        )
        SELECT
            COALESCE(vector_search.id, fulltext_search.id) AS id,
            COALESCE(1.0 / (:k + vector_search.rank), 0.0) +
            COALESCE(1.0 / (:k + fulltext_search.rank), 0.0) AS score
        FROM vector_search
        FULL OUTER JOIN fulltext_search ON vector_search.id = fulltext_search.id
        ORDER BY score DESC
        LIMIT 20
        """

        if query_text is not None and len(query_vector) > 0:
            sql = text(hybrid_query).columns(
                column("id", Integer), column("score", Float)
            )
        elif len(query_vector) > 0:
            sql = text(vector_query).columns(
                column("id", Integer), column("rank", Integer)
            )
        elif query_text is not None:
            sql = text(fulltext_query).columns(
                column("id", Integer), column("rank", Integer)
            )
        else:
            raise ValueError("Both query text and query vector are empty")

        results = []
        with get_db_session() as db_session:
            results = (
                db_session.execute(
                    sql,
                    {"embedding": str(query_vector), "query": query_text, "k": 60},
                )
            ).fetchall()

        # Convert results to models
        items = []
        for id, _ in results[:top]:
            with get_db_session() as db_session:
                if table_name == "menu_item":
                    item = db_session.execute(
                        select(self.db_model)
                        .where(self.db_model.id == id)
                        .options(joinedload(self.db_model.options))
                    )
                else:
                    item = db_session.execute(
                        select(self.db_model).where(self.db_model.id == id)
                    )
                items.append(item.scalar())
        return items

    def search_and_embed(
        self,
        query_text: Union[str, None] = None,
        top: int = 5,
        enable_vector_search: bool = True,
        enable_text_search: bool = True,
        filters: Union[list[dict], None] = None,
    ):
        """
        Search items by query text. Optionally converts the query text to a
        vector if enable_vector_search is True.
        """
        vector: list[float] = []
        if enable_vector_search and query_text is not None:
            vector = embedding_util.generate(
                query_text,
                self.embed_dimensions,
            )
        if not enable_text_search:
            query_text = None

        return self.search(query_text, vector, top, filters)
