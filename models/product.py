"""
    This module contains SQLAlchemy model for the product data model.
"""

from __future__ import annotations
import datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy import Index, Column, Integer, String, DateTime, ARRAY, Text

from models.database import engine
from models import Base

class Product(Base):
    __tablename__ = "Product"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    category = Column(String)
    price = Column(Integer)
    currency = Column(String)
    available_stock = Column(Integer)
    rating = Column(Integer)
    age_group = Column(String)
    sizes = Column(ARRAY(String))
    embedding = Column(Vector(1536))
    content = Column(Text)
    created_at= Column(DateTime, default=datetime.datetime.utcnow)

    def to_str(self):
        res = f"Product: {self.name}\n"
        res += f"Description: {self.description}\n"
        res += f"Category: {self.category}\n"
        res += f"Price: {self.price} {self.currency}\n"
        res += f"Available Stock: {self.available_stock}\n"
        res += f"Rating: {self.rating}\n"
        res += f"Age Group: {self.age_group}\n"
        res += f"Sizes: {', '.join(self.sizes)}\n"
        return res
    
    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "price": self.price,
            "currency": self.currency,
            "available_stock": self.available_stock,
            "rating": self.rating,
            "age_group": self.age_group,
            "sizes": self.sizes,
        }

    @staticmethod
    def get_text_search_field():
        return "content"

    @staticmethod
    def get_embedding_field():
        return "embedding"

index_ada002 = Index(
    "hnsw_index_for_innerproduct_product_embedding_ada002",
    Product.embedding,
    postgresql_using="hnsw",
    postgresql_with={"m": 16, "ef_construction": 64},
    postgresql_ops={"embedding": "vector_l2_ops"},
)

# Just create tables
Base.metadata.create_all(engine)
