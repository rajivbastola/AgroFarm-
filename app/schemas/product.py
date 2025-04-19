from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.models.product import ProductCategory

class ProductBase(BaseModel):
    name: str
    description: str
    price: float = Field(gt=0)
    stock_quantity: int = Field(ge=0)
    category: ProductCategory
    unit: str
    image_url: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    stock_quantity: Optional[int] = Field(None, ge=0)
    category: Optional[ProductCategory] = None
    unit: Optional[str] = None
    image_url: Optional[str] = None

class Product(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PaginatedProducts(BaseModel):
    items: List[Product]
    total: int
    page: int
    total_pages: int
    has_more: bool

    class Config:
        from_attributes = True