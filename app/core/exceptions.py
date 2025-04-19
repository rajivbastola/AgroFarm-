from typing import Any, Optional
from fastapi import HTTPException, status

class AgroFarmException(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: Any = None,
        headers: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail, headers=headers)

class ProductNotFound(AgroFarmException):
    def __init__(self, product_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )

class InsufficientStock(AgroFarmException):
    def __init__(self, product_name: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient stock for product: {product_name}"
        )

class OrderNotFound(AgroFarmException):
    def __init__(self, order_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID {order_id} not found"
        )

class InvalidOrderStatus(AgroFarmException):
    def __init__(self, current_status: str, allowed_status: list[str]):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot change order in {current_status} status. Allowed statuses: {', '.join(allowed_status)}"
        )

class NotAuthorized(AgroFarmException):
    def __init__(self, message: str = "Not authorized to perform this action"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=message
        )