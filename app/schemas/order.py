from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from app.models.order import OrderStatus

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    id: int
    order_id: int
    unit_price: float
    created_at: datetime

    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    shipping_address: str
    contact_phone: str

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    shipping_address: Optional[str] = None
    contact_phone: Optional[str] = None

class Order(OrderBase):
    id: int
    user_id: int
    total_amount: float
    status: OrderStatus
    items: List[OrderItem]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True