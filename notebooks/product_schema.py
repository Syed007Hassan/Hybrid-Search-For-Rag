"""
This module contains the Pydantic schema for the product data model.
"""

# pylint:disable=missing-class-docstring,missing-function-docstring

from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field


class CurrencyEnum(str, Enum):
    PKR = "PKR"
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"


class Product(BaseModel):
    name: str = Field(..., description="Product name")
    description: str = Field(..., description="Detailed description of the product")
    category: str = Field(..., description="Category of the product")
    price: float = Field(..., description="Price of the product")
    currency: CurrencyEnum = Field(..., description="Currency of the product price")
    available_stock: int = Field(..., description="Number of units available in stock")
    rating: Optional[float] = Field(None, description="Product rating out of 5")
    age_group: Optional[str] = Field(
        None, description="Age group for which the product is suitable. Eg 10-15"
    )
    sizes: Optional[List[str]] = Field(
        None, description="Available sizes for the product"
    )


class ProductsSchema(BaseModel):
    products: List[Product]
