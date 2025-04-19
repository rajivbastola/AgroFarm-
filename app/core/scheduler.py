from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from loguru import logger
from pathlib import Path
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.product import Product
from app.models.order import Order, OrderStatus
from app.utils.file_upload import UPLOAD_DIR
import os

# Initialize scheduler
scheduler = AsyncIOScheduler()

async def cleanup_old_files():
    """Clean up unused files older than 7 days"""
    try:
        cutoff = datetime.now() - timedelta(days=7)
        
        for root, _, files in os.walk(UPLOAD_DIR):
            for file in files:
                file_path = Path(root) / file
                if file_path.stat().st_mtime < cutoff.timestamp():
                    # Check if file is still referenced in database
                    db = SessionLocal()
                    try:
                        product = db.query(Product).filter(
                            Product.image_url.contains(file)
                        ).first()
                        
                        if not product:
                            os.remove(file_path)
                            logger.info(f"Removed unused file: {file_path}")
                    finally:
                        db.close()
    
    except Exception as e:
        logger.error(f"Error in cleanup_old_files: {str(e)}")

async def check_low_inventory():
    """Check for products with low inventory and log warnings"""
    try:
        db = SessionLocal()
        try:
            low_stock_products = db.query(Product).filter(
                Product.stock_quantity <= 10
            ).all()
            
            for product in low_stock_products:
                logger.warning(
                    f"Low inventory alert: Product {product.name} "
                    f"(ID: {product.id}) has only {product.stock_quantity} units left"
                )
        finally:
            db.close()
    
    except Exception as e:
        logger.error(f"Error in check_low_inventory: {str(e)}")

async def check_stalled_orders():
    """Check for orders that have been in the same status for too long"""
    try:
        db = SessionLocal()
        try:
            # Check orders that haven't moved from PENDING in 24 hours
            cutoff = datetime.utcnow() - timedelta(hours=24)
            stalled_orders = db.query(Order).filter(
                Order.status == OrderStatus.PENDING,
                Order.created_at < cutoff
            ).all()
            
            for order in stalled_orders:
                logger.warning(
                    f"Stalled order alert: Order {order.id} has been "
                    f"in PENDING status since {order.created_at}"
                )
            
            # Check orders that haven't moved from PROCESSING in 48 hours
            cutoff = datetime.utcnow() - timedelta(hours=48)
            processing_orders = db.query(Order).filter(
                Order.status == OrderStatus.PROCESSING,
                Order.updated_at < cutoff
            ).all()
            
            for order in processing_orders:
                logger.warning(
                    f"Stalled order alert: Order {order.id} has been "
                    f"in PROCESSING status since {order.updated_at}"
                )
        
        finally:
            db.close()
    
    except Exception as e:
        logger.error(f"Error in check_stalled_orders: {str(e)}")

def init_scheduler(app: FastAPI):
    """Initialize and start the scheduler with all jobs"""
    
    # Add jobs to scheduler
    scheduler.add_job(
        cleanup_old_files,
        CronTrigger(hour=3, minute=0),  # Run at 3 AM every day
        id='cleanup_old_files',
        name='Clean up unused files',
        misfire_grace_time=3600  # Allow job to be run up to 1 hour late
    )
    
    scheduler.add_job(
        check_low_inventory,
        IntervalTrigger(hours=6),  # Run every 6 hours
        id='check_low_inventory',
        name='Check low inventory',
        misfire_grace_time=3600
    )
    
    scheduler.add_job(
        check_stalled_orders,
        IntervalTrigger(hours=4),  # Run every 4 hours
        id='check_stalled_orders',
        name='Check stalled orders',
        misfire_grace_time=3600
    )
    
    # Start scheduler
    scheduler.start()
    
    # Shutdown event handler
    @app.on_event("shutdown")
    async def shutdown_scheduler():
        scheduler.shutdown()