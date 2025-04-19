from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.core.config import settings
from app.utils.email_templates import get_order_status_template
from app.models.order import Order, OrderStatus
from pathlib import Path
from jinja2 import Environment, select_autoescape, PackageLoader
import aiofiles
from fastapi import BackgroundTasks
from loguru import logger

# Email configuration
conf = ConnectionConfig(
    MAIL_USERNAME=settings.SMTP_USER,
    MAIL_PASSWORD=settings.SMTP_PASSWORD,
    MAIL_FROM=settings.EMAILS_FROM_EMAIL,
    MAIL_FROM_NAME=settings.EMAILS_FROM_NAME,
    MAIL_PORT=settings.SMTP_PORT,
    MAIL_SERVER=settings.SMTP_HOST,
    MAIL_TLS=settings.SMTP_TLS,
    MAIL_SSL=False,
    TEMPLATE_FOLDER=Path(__file__).parent / 'email_templates'
)

# Initialize FastMail
fastmail = FastMail(conf)

async def send_email_async(
    email_to: str,
    subject: str,
    body: str,
    background_tasks: BackgroundTasks
):
    """Send email asynchronously using background tasks"""
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        body=body,
        subtype="html"
    )
    
    try:
        background_tasks.add_task(fastmail.send_message, message)
        logger.info(f"Email queued for sending to {email_to}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email to {email_to}: {str(e)}")
        return False

async def send_order_status_email(
    order: Order,
    background_tasks: BackgroundTasks,
    tracking_number: str = None,
    cancel_reason: str = None
):
    """Send order status update email to customer"""
    template = get_order_status_template(order.status)
    
    # Prepare template variables
    template_vars = {
        "customer_name": order.user.full_name,
        "order_id": order.id,
        "total_amount": order.total_amount,
        "status": order.status.value,
        "tracking_number": tracking_number,
        "cancel_reason": cancel_reason,
        "delivery_date": order.updated_at.strftime("%Y-%m-%d") if order.status == OrderStatus.DELIVERED else None
    }
    
    # Format email body with template variables
    body = template["body"].format(**template_vars)
    
    # Send email
    return await send_email_async(
        email_to=order.user.email,
        subject=template["subject"],
        body=body,
        background_tasks=background_tasks
    )

async def send_welcome_email(
    user_email: str,
    user_name: str,
    background_tasks: BackgroundTasks
):
    """Send welcome email to new users"""
    subject = "Welcome to Agro Farm!"
    body = f"""
    <h2>Welcome to Agro Farm, {user_name}!</h2>
    <p>Thank you for joining our community of farmers and food enthusiasts.</p>
    <p>With your account, you can:</p>
    <ul>
        <li>Browse fresh farm products</li>
        <li>Place orders for delivery</li>
        <li>Track your orders</li>
        <li>Support local farmers</li>
    </ul>
    <p>If you have any questions, feel free to contact our support team.</p>
    <p>Happy shopping!</p>
    """
    
    return await send_email_async(
        email_to=user_email,
        subject=subject,
        body=body,
        background_tasks=background_tasks
    )