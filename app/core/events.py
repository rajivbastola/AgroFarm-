from typing import Callable, Dict, List
from app.models.order import OrderStatus
from loguru import logger

class EventManager:
    def __init__(self):
        self.handlers: Dict[str, List[Callable]] = {}
    
    def subscribe(self, event_type: str, handler: Callable) -> None:
        """Subscribe a handler to an event type"""
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        self.handlers[event_type].append(handler)
    
    async def publish(self, event_type: str, **kwargs) -> None:
        """Publish an event to all subscribed handlers"""
        if event_type in self.handlers:
            for handler in self.handlers[event_type]:
                try:
                    await handler(**kwargs)
                except Exception as e:
                    logger.error(f"Error in event handler: {str(e)}")

# Create global event manager instance
event_manager = EventManager()

# Event types
class OrderEvents:
    STATUS_CHANGED = "order.status_changed"
    CREATED = "order.created"
    CANCELLED = "order.cancelled"

# Example event handlers
async def log_order_status_change(order_id: int, old_status: OrderStatus, new_status: OrderStatus) -> None:
    """Log order status changes"""
    logger.info(f"Order {order_id} status changed from {old_status} to {new_status}")

async def notify_customer_order_status(order_id: int, new_status: OrderStatus, user_email: str) -> None:
    """Send notification to customer about order status change"""
    # This is a placeholder for email notification logic
    logger.info(f"Notification sent to {user_email} for order {order_id}: Status changed to {new_status}")

async def handle_order_cancellation(order_id: int, reason: str = None) -> None:
    """Handle order cancellation tasks"""
    logger.info(f"Order {order_id} cancelled. Reason: {reason or 'Not specified'}")

# Register default event handlers
event_manager.subscribe(OrderEvents.STATUS_CHANGED, log_order_status_change)
event_manager.subscribe(OrderEvents.STATUS_CHANGED, notify_customer_order_status)
event_manager.subscribe(OrderEvents.CANCELLED, handle_order_cancellation)