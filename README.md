# Agro Farm E-Commerce API

A FastAPI-based backend API for an e-commerce platform that connects local farmers with urban buyers. The platform enables direct sale of fresh agro products, including vegetables, fruits, dairy, and grains.

## Features

- 🔐 JWT-based authentication
- 👤 User registration and management
- 🏪 Product catalog with categories
- 🛒 Order management system
- 📦 Real-time inventory tracking
- 🔍 Product search and filtering
- 👨‍💼 Admin dashboard capabilities
- 📱 RESTful API for frontend integration

## Tech Stack

- Backend: FastAPI (Python 3.10+)
- Authentication: OAuth2 with JWT tokens
- Database: SQLite (dev) / PostgreSQL (prod)
- ORM: SQLAlchemy
- Validation: Pydantic
- Testing: Pytest

## Getting Started

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd ecommerce
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configurations
   ```

### Running the Application

1. Start the development server:
   ```bash
   uvicorn app.main:app --reload
   ```

2. Access the API documentation:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Running Tests

```bash
pytest app/tests
```

## API Endpoints

### Authentication
- POST `/api/auth/register` - Register new user
- POST `/api/auth/login` - Login and get JWT token

### Products
- GET `/api/products` - List all products
- GET `/api/products/{id}` - Get product details
- POST `/api/products` - Create new product (Admin only)
- PUT `/api/products/{id}` - Update product (Admin only)
- DELETE `/api/products/{id}` - Delete product (Admin only)

### Orders
- POST `/api/orders` - Create new order
- GET `/api/orders` - List user's orders
- GET `/api/orders/{id}` - Get order details
- PUT `/api/orders/{id}` - Update order status (Admin only)
- POST `/api/orders/{id}/cancel` - Cancel order

## Development

### Project Structure
```
app/
├── core/           # Core functionality
├── models/         # SQLAlchemy models
├── schemas/        # Pydantic schemas
├── routers/        # API endpoints
├── tests/          # Test suite
└── utils/          # Utility functions
```

### Database Migrations

The project uses SQLite for development. For production, it's recommended to switch to PostgreSQL:

1. Update the `SQLALCHEMY_DATABASE_URL` in `.env`
2. The tables will be automatically created on first run

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Future Enhancements

- [ ] Subscription orders (weekly baskets)
- [ ] Admin dashboard with analytics
- [ ] Email/SMS notification system
- [ ] Delivery tracking
- [ ] Payment gateway integration
- [ ] Product reviews and ratings
- [ ] Multi-language support

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Rajiv Bastola