from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from typing import Optional, Literal
from ..utils.database import get_db
from ..models.product import Product
from ..schemas.product import PaginatedProducts

router = APIRouter()

@router.get("/products", response_model=PaginatedProducts)
async def get_products(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=12, ge=1, le=100),
    min_price: Optional[float] = Query(default=None, ge=0),
    max_price: Optional[float] = Query(default=None, ge=0),
    category: Optional[str] = None,
    sort_by: Optional[Literal["price", "name", "created_at"]] = None,
    sort_order: Optional[Literal["asc", "desc"]] = "asc",
    db: Session = Depends(get_db)
):
    query = db.query(Product)
    
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    if category:
        query = query.filter(Product.category == category)
    
    total = query.count()
    
    if sort_by:
        order_column = getattr(Product, sort_by)
        query = query.order_by(desc(order_column) if sort_order == "desc" else asc(order_column))
    
    products = query.offset(skip).limit(limit).all()
    
    page = (skip // limit) + 1
    total_pages = (total + limit - 1) // limit if limit else 1
    has_more = (skip + limit) < total
    
    return PaginatedProducts(
        items=products,
        total=total,
        page=page,
        total_pages=total_pages,
        has_more=has_more
    )