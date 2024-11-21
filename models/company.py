from __future__ import annotations
import datetime
from pgvector.sqlalchemy import Vector
from sqlalchemy import Index, Column, Integer, String, DateTime, Text
from models.database import engine
from models import Base

class Company(Base):
    __tablename__ = "Company"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    industry = Column(String)
    size = Column(String)
    location = Column(String)
    embedding = Column(Vector(1536))
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    def to_str(self):
        return f"Company: {self.name}\nDescription: {self.description}\nIndustry: {self.industry}\nSize: {self.size}\nLocation: {self.location}"
    
    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "industry": self.industry,
            "size": self.size,
            "location": self.location,
        }

    @staticmethod
    def get_text_search_field():
        return "content"

    @staticmethod
    def get_embedding_field():
        return "embedding"

index_ada002 = Index(
    "hnsw_index_for_innerproduct_company_embedding_ada002",
    Company.embedding,
    postgresql_using="hnsw", # hnsw is a hybrid search index that is faster than the default btree index
    postgresql_with={"m": 16, "ef_construction": 64},
    postgresql_ops={"embedding": "vector_l2_ops"},
)

Base.metadata.create_all(engine) 