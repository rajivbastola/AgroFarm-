from sqlalchemy.orm import Session
from ..models.product import Product
from .database import SessionLocal

def init_db():
    db = SessionLocal()
    try:
        # Check if we already have products
        if db.query(Product).first() is None:
            sample_products = [
                Product(
                    name="Organic Tomatoes",
                    description="Fresh organic tomatoes from local farms",
                    price=2.99,
                    stock=100,
                    category="Vegetables",
                    image_url="https://example.com/tomatoes.jpg"
                ),
                Product(
                    name="Farm Fresh Eggs",
                    description="Free-range eggs from happy chickens",
                    price=4.99,
                    stock=50,
                    category="Dairy & Eggs",
                    image_url="https://example.com/eggs.jpg"
                ),
                Product(
                    name="Honey",
                    description="Raw, unfiltered local honey",
                    price=8.99,
                    stock=30,
                    category="Sweeteners",
                    image_url="https://example.com/honey.jpg"
                ),
                Product(
                    name="Organic Carrots",
                    description="Fresh organic carrots",
                    price=1.99,
                    stock=150,
                    category="Vegetables",
                    image_url="https://example.com/carrots.jpg"
                ),
                Product(
                    name="Fresh Basil",
                    description="Aromatic fresh basil",
                    price=3.49,
                    stock=40,
                    category="Herbs",
                    image_url="https://example.com/basil.jpg"
                )
            ]
            for product in sample_products:
                db.add(product)
            db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()