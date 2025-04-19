from typing import List
from app.models.order import OrderStatus

class OrderStatusTransition:
    ALLOWED_TRANSITIONS = {
        OrderStatus.PENDING: [OrderStatus.CONFIRMED, OrderStatus.CANCELLED],
        OrderStatus.CONFIRMED: [OrderStatus.PROCESSING, OrderStatus.CANCELLED],
        OrderStatus.PROCESSING: [OrderStatus.SHIPPED, OrderStatus.CANCELLED],
        OrderStatus.SHIPPED: [OrderStatus.DELIVERED],
        OrderStatus.DELIVERED: [],  # Final state
        OrderStatus.CANCELLED: []   # Final state
    }

    @staticmethod
    def get_allowed_transitions(current_status: OrderStatus) -> List[OrderStatus]:
        """Get allowed next status transitions for current order status."""
        return OrderStatusTransition.ALLOWED_TRANSITIONS.get(current_status, [])

    @staticmethod
    def can_transition_to(current_status: OrderStatus, new_status: OrderStatus) -> bool:
        """Check if order can transition from current status to new status."""
        allowed = OrderStatusTransition.get_allowed_transitions(current_status)
        return new_status in allowed

    @staticmethod
    def validate_transition(current_status: OrderStatus, new_status: OrderStatus) -> None:
        """Validate order status transition. Raises InvalidOrderStatus if not allowed."""
        from app.core.exceptions import InvalidOrderStatus
        
        if not OrderStatusTransition.can_transition_to(current_status, new_status):
            allowed = [s.value for s in OrderStatusTransition.get_allowed_transitions(current_status)]
            raise InvalidOrderStatus(current_status.value, allowed)

    @staticmethod
    def is_final_state(status: OrderStatus) -> bool:
        """Check if the given status is a final state."""
        return not OrderStatusTransition.get_allowed_transitions(status)