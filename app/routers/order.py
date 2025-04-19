from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.deps import get_current_user, get_current_active_admin, get_db
from app.core.pagination import Page, PageParams, paginate
from app.core.exceptions import OrderNotFound, NotAuthorized, InsufficientStock
from app.core.order_utils import OrderStatusTransition
from app.models.order import Order, OrderItem, OrderStatus
from app.models.product import Product
from app.models.user import User
from app.schemas.order import OrderCreate, OrderUpdate, Order as OrderSchema

router = APIRouter(prefix="/orders", tags=["orders"])

@router.get("/", response_model=Page[OrderSchema])
async def list_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    params: PageParams = Depends(),
    status: OrderStatus = None
):
    """
    List orders with pagination.
    Admins can see all orders, regular users see only their orders.
    """
    query = db.query(Order)
    if not current_user.is_admin:
        query = query.filter(Order.user_id == current_user.id)
    if status:
        query = query.filter(Order.status == status)
    query = query.order_by(Order.created_at.desc())
    return paginate(query, params)

@router.get("/{order_id}", response_model=OrderSchema)
async def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get order details.
    Users can only access their own orders, admins can access any order.
    """
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise OrderNotFound(order_id)
    if not current_user.is_admin and order.user_id != current_user.id:
        raise NotAuthorized("Not authorized to access this order")
    return order

@router.post("/", response_model=OrderSchema)
async def create_order(
    order_in: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new order.
    Validates stock availability and updates product quantities.
    """
    # Calculate total amount and validate stock
    total_amount = 0
    order_items = []
    
    for item in order_in.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise ProductNotFound(item.product_id)
        if product.stock_quantity < item.quantity:
            raise InsufficientStock(product.name)
        
        # Update stock quantity
        product.stock_quantity -= item.quantity
        total_amount += product.price * item.quantity
        
        order_items.append({
            "product_id": item.product_id,
            "quantity": item.quantity,
            "unit_price": product.price
        })
    
    # Create order
    db_order = Order(
        user_id=current_user.id,
        total_amount=total_amount,
        status=OrderStatus.PENDING,
        shipping_address=order_in.shipping_address,
        contact_phone=order_in.contact_phone
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    # Create order items
    for item_data in order_items:
        db_item = OrderItem(order_id=db_order.id, **item_data)
        db.add(db_item)
    
    db.commit()
    db.refresh(db_order)
    return db_order

@router.put("/{order_id}/status", response_model=OrderSchema)
async def update_order_status(
    order_id: int,
    status: OrderStatus,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_admin)
):
    """
    Update order status (admin only).
    Validates status transitions according to the defined workflow.
    """
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise OrderNotFound(order_id)
    
    OrderStatusTransition.validate_transition(order.status, status)
    order.status = status
    db.commit()
    db.refresh(order)
    return order

@router.post("/{order_id}/cancel", response_model=OrderSchema)
async def cancel_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Cancel an order.
    Users can cancel their own pending orders, admins can cancel any order.
    """
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise OrderNotFound(order_id)
    
    if not current_user.is_admin and order.user_id != current_user.id:
        raise NotAuthorized("Not authorized to cancel this order")
    
    try:
        OrderStatusTransition.validate_transition(order.status, OrderStatus.CANCELLED)
    except InvalidOrderStatus:
        raise InvalidOrderStatus(
            order.status.value,
            ["Cannot cancel order in current status"]
        )
    
    # Restore product quantities
    for item in order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product:
            product.stock_quantity += item.quantity
    
    order.status = OrderStatus.CANCELLED
    db.commit()
    db.refresh(order)
    return order

@router.get("/status/transitions")
async def get_status_transitions():
    """
    Get the allowed order status transitions for each status.
    Useful for frontend to show valid status options.
    """
    return {
        status.value: [s.value for s in OrderStatusTransition.get_allowed_transitions(status)]
        for status in OrderStatus
    }