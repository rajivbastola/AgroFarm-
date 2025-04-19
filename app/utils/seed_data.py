from sqlalchemy.orm import Session
from app.core.security import get_password_hash
from app.models.user import User
from app.models.product import Product, ProductCategory

def seed_initial_data(db: Session) -> None:
    # Create admin user if it doesn't exist
    admin_email = "admin@agrofarm.com"
    if not db.query(User).filter(User.email == admin_email).first():
        admin_user = User(
            email=admin_email,
            full_name="Admin User",
            hashed_password=get_password_hash("admin123"),
            is_admin=True
        )
        db.add(admin_user)
        db.commit()

    # Add sample products if none exist
    if db.query(Product).count() == 0:
        sample_products = [
            {
                "name": "Fresh Tomatoes",
                "description": "Organically grown tomatoes from local farms",
                "price": 2.99,
                "stock_quantity": 100,
                "category": ProductCategory.VEGETABLES,
                "unit": "kg"
            },
            {
                "name": "Organic Apples",
                "description": "Sweet and crispy apples from hill orchards",
                "price": 3.99,
                "stock_quantity": 150,
                "category": ProductCategory.FRUITS,
                "unit": "kg"
            },
            {
                "name": "Farm Fresh Milk",
                "description": "Pure cow milk from grass-fed cows",
                "price": 1.99,
                "stock_quantity": 50,
                "category": ProductCategory.DAIRY,
                "unit": "liter"
            },
            {
                "name": "Organic Rice",
                "description": "Premium quality basmati rice",
                "price": 5.99,
                "stock_quantity": 200,
                "category": ProductCategory.GRAINS,
                "unit": "kg"
            }
        ]

        for product_data in sample_products:
            product = Product(**product_data)
            db.add(product)
        
        db.commit()