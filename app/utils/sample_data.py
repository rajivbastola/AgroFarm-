from sqlalchemy.orm import Session
from ..models.product import Product
from ..utils.database import get_db, engine

def add_sample_products(db: Session):
    sample_products = [
        {
            "name": "Organic Tomatoes",
            "description": "Fresh, locally grown organic tomatoes. Perfect for salads and cooking.",
            "price": 3.99,
            "stock": 100,
            "category": "Vegetables",
            "image_url": "https://example.com/images/tomatoes.jpg"
        },
        {
            "name": "Fresh Strawberries",
            "description": "Sweet and juicy strawberries, harvested daily from our farm.",
            "price": 4.99,
            "stock": 50,
            "category": "Fruits",
            "image_url": "https://example.com/images/strawberries.jpg"
        },
        {
            "name": "Organic Carrots",
            "description": "Crisp, organic carrots rich in vitamins and minerals.",
            "price": 2.99,
            "stock": 150,
            "category": "Vegetables",
            "image_url": "https://example.com/images/carrots.jpg"
        },
        {
            "name": "Farm Fresh Eggs",
            "description": "Free-range chicken eggs, collected daily.",
            "price": 5.99,
            "stock": 200,
            "category": "Dairy & Eggs",
            "image_url": "https://example.com/images/eggs.jpg"
        },
        {
            "name": "Organic Honey",
            "description": "Pure, raw honey from our local bee farm.",
            "price": 8.99,
            "stock": 75,
            "category": "Natural Sweeteners",
            "image_url": "https://example.com/images/honey.jpg"
        }
    ]
    
    for product_data in sample_products:
        product = Product(**product_data)
        db.add(product)
    
    try:
        db.commit()
        print("Sample products added successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error adding sample products: {e}")

if __name__ == "__main__":
    db = next(get_db())
    add_sample_products(db)