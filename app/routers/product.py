from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status, UploadFile, File, BackgroundTasks
from sqlalchemy.orm import Session
from app.core.deps import get_current_user, get_current_active_admin, get_db
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate, Product as ProductSchema
from app.models.user import User
from app.core.pagination import Page, PageParams, paginate
from app.core.search import filter_products
from app.core.exceptions import ProductNotFound
from app.models.product import Product, ProductCategory
from app.utils.file_upload import save_upload_file, delete_file, get_file_url
from app.core.docs import generate_response_schema
from app.core.security_utils import cache_response

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model=Page[ProductSchema])
@cache_response(expire_after_seconds=300, key_prefix="products", vary_on_headers=["authorization"])
async def list_products(
    *,
    db: Session = Depends(get_db),
    params: PageParams = Depends(),
    search: Optional[str] = None,
    category: Optional[ProductCategory] = None,
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    in_stock: Optional[bool] = None
):
    """
    List products with filtering and pagination.
    - **search**: Search in product name and description
    - **category**: Filter by product category
    - **min_price**: Minimum price filter
    - **max_price**: Maximum price filter
    - **in_stock**: Filter by stock availability
    """
    query = db.query(Product)
    query = filter_products(
        query=query,
        search=search,
        category=category,
        min_price=min_price,
        max_price=max_price,
        in_stock=in_stock
    )
    return paginate(query, params)

@router.get("/{product_id}", response_model=ProductSchema)
@cache_response(expire_after_seconds=300, key_prefix="product")
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """
    Get a specific product by ID.
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise ProductNotFound(product_id)
    return product

@router.post("/", response_model=ProductSchema)
async def create_product(
    product_in: ProductCreate,
    db: Session = Depends(get_db),
    _: None = Depends(get_current_active_admin)
):
    """
    Create a new product (admin only).
    """
    product = Product(**product_in.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@router.post("/{product_id}/image")
async def upload_product_image(
    product_id: int,
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    _: None = Depends(get_current_active_admin),
    background_tasks: BackgroundTasks = None
):
    """
    Upload a product image (admin only).
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise ProductNotFound(product_id)
    
    try:
        # Delete old image if exists
        if product.image_url:
            background_tasks.add_task(delete_file, product.image_url)
        
        # Save new image
        file_path = await save_upload_file(image)
        product.image_url = file_path
        db.commit()
        
        return {
            "message": "Image uploaded successfully",
            "image_url": get_file_url(file_path)
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error uploading image")

@router.put("/{product_id}", response_model=ProductSchema)
async def update_product(
    product_id: int,
    product_in: ProductUpdate,
    db: Session = Depends(get_db),
    _: None = Depends(get_current_active_admin)
):
    """
    Update a product (admin only).
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise ProductNotFound(product_id)
    
    update_data = product_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)
    
    db.commit()
    db.refresh(product)
    return product

@router.delete("/{product_id}")
async def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    _: None = Depends(get_current_active_admin),
    background_tasks: BackgroundTasks = None
):
    """
    Delete a product (admin only).
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise ProductNotFound(product_id)
    
    # Delete product image if exists
    if product.image_url:
        background_tasks.add_task(delete_file, product.image_url)
    
    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}

@router.get("/categories/list")
@cache_response(expire_after_seconds=3600, key_prefix="categories")
async def list_categories():
    """
    List all available product categories.
    """
    return [{"value": category.value, "label": category.name} for category in ProductCategory]