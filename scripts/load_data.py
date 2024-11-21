"""
    This file loads the data from sample_products.json
    and inserts it into the database.
"""

import json
import sys
sys.path.append(".")

from models.company import Company
from models.database import get_db_session
from services.embedding import Embedding

embedding_service = Embedding()


def load_data():
    """
    This function is used to load the data from sample_products.json
    and insert it into the database.
    """
    with open("scripts/sample_companies.json", "r") as f: #pylint: disable=unspecified-encoding
        data = json.load(f)
        data = data["companies"]
    with get_db_session() as session:
        for item in data:
            company = Company(**item)
            company.content = company.to_str()
            company.embedding = embedding_service.generate(company.content)
            session.add(company)
        session.commit()


if __name__ == "__main__":
    load_data()
