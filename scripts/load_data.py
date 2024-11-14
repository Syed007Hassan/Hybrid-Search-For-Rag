"""
    This file loads the data from sample_products.json
    and inserts it into the database.
"""

import json
import sys
sys.path.append(".")

from models.product import Product
from models.database import get_db_session
from services.embedding import Embedding

embedding_service = Embedding()


def load_data():
    """
    This function is used to load the data from sample_products.json
    and insert it into the database.
    """
    with open("scripts/sample_products.json", "r") as f: #pylint: disable=unspecified-encoding
        data = json.load(f)
        data = data["products"]
    with get_db_session() as session:
        for item in data:
            product = Product(**item)
            product.content = product.to_str()
            product.embedding = embedding_service.generate(product.content)
            session.add(product)
        session.commit()


if __name__ == "__main__":
    load_data()
