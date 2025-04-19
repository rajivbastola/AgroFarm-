from typing import Generic, List, TypeVar
from fastapi import Query
from pydantic import BaseModel
from sqlalchemy.orm import Query as SQLAlchemyQuery

T = TypeVar("T")

class PageParams:
    def __init__(
        self,
        skip: int = Query(0, ge=0),
        limit: int = Query(10, ge=1, le=100)
    ):
        self.skip = skip
        self.limit = limit

class Page(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int
    pages: int

    class Config:
        from_attributes = True

def paginate(query: SQLAlchemyQuery, params: PageParams) -> Page:
    total = query.count()
    items = query.offset(params.skip).limit(params.limit).all()
    
    return Page(
        items=items,
        total=total,
        page=(params.skip // params.limit) + 1,
        size=params.limit,
        pages=-(-total // params.limit)  # Ceiling division
    )