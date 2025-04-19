from typing import Dict
from app.models.order import OrderStatus

def get_order_status_template(status: OrderStatus) -> Dict[str, str]:
    """Get email template for order status updates"""
    templates = {
        OrderStatus.CONFIRMED: {
            "subject": "Your Order Has Been Confirmed",
            "body": """
            Dear {customer_name},

            Great news! Your order #{order_id} has been confirmed and is being processed.

            Order Details:
            - Order ID: {order_id}
            - Total Amount: ${total_amount:.2f}
            - Status: Confirmed

            We'll notify you when your order is ready for shipping.

            Thank you for choosing Agro Farm!
            """
        },
        OrderStatus.PROCESSING: {
            "subject": "Your Order is Being Processed",
            "body": """
            Dear {customer_name},

            Your order #{order_id} is now being processed and prepared for shipping.

            Order Details:
            - Order ID: {order_id}
            - Total Amount: ${total_amount:.2f}
            - Status: Processing

            We'll update you once your order has been shipped.

            Thank you for your patience!
            """
        },
        OrderStatus.SHIPPED: {
            "subject": "Your Order Has Been Shipped",
            "body": """
            Dear {customer_name},

            Your order #{order_id} is on its way to you!

            Order Details:
            - Order ID: {order_id}
            - Total Amount: ${total_amount:.2f}
            - Status: Shipped
            - Tracking Number: {tracking_number}

            You can track your order using the tracking number above.

            Thank you for shopping with Agro Farm!
            """
        },
        OrderStatus.DELIVERED: {
            "subject": "Your Order Has Been Delivered",
            "body": """
            Dear {customer_name},

            Your order #{order_id} has been delivered successfully.

            Order Details:
            - Order ID: {order_id}
            - Total Amount: ${total_amount:.2f}
            - Status: Delivered
            - Delivery Date: {delivery_date}

            We hope you enjoy your fresh farm products! Please don't hesitate to contact us if you have any questions.

            Thank you for choosing Agro Farm!
            """
        },
        OrderStatus.CANCELLED: {
            "subject": "Your Order Has Been Cancelled",
            "body": """
            Dear {customer_name},

            Your order #{order_id} has been cancelled.

            Order Details:
            - Order ID: {order_id}
            - Total Amount: ${total_amount:.2f}
            - Status: Cancelled
            - Reason: {cancel_reason}

            If you didn't request this cancellation or have any questions, please contact our support team.

            Thank you for your understanding.
            """
        }
    }
    
    return templates.get(status, {
        "subject": "Order Status Update",
        "body": """
        Dear {customer_name},

        Your order #{order_id} has been updated.

        Order Details:
        - Order ID: {order_id}
        - Total Amount: ${total_amount:.2f}
        - Status: {status}

        Thank you for shopping with Agro Farm!
        """
    })