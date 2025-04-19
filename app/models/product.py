from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.core.database import Base

class ProductCategory(enum.Enum):
    VEGETABLES = "vegetables"
    FRUITS = "fruits"
    DAIRY = "dairy"
    GRAINS = "grains"
    OTHER = "other"

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    price = Column(Float)
    stock_quantity = Column(Integer)
    category = Column(Enum(ProductCategory))
    unit = Column(String)  # e.g., kg, pieces, litres
    image_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    order_items = relationship("OrderItem", back_populates="product")