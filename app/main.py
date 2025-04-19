from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.core.logging import setup_logging, RequestLoggingMiddleware
from app.core.docs import api_tags_metadata
from app.routers import auth, product, order
from app.core.database import engine, SessionLocal
from app.models import user, product as product_model, order as order_model
from app.utils.seed_data import seed_initial_data
from app.core.middleware import error_handler
from datetime import datetime
from pathlib import Path

# Setup logging
setup_logging()

# Create database tables
user.Base.metadata.create_all(bind=engine)
product_model.Base.metadata.create_all(bind=engine)
order_model.Base.metadata.create_all(bind=engine)

# Seed initial data
db = SessionLocal()
seed_initial_data(db)
db.close()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=api_tags_metadata,
    description="""
    🌾 Agro Farm E-Commerce API

    Connect local farmers with urban buyers through a modern e-commerce platform.
    
    Key features:
    * 👤 User authentication with JWT
    * 🏪 Product management with real-time inventory
    * 📦 Order processing and tracking
    * 💰 Secure payment integration (coming soon)
    * 📱 Mobile-friendly API design
    """,
    version="1.0.0"
)

# CORS configuration
origins = [
    "http://localhost:3000",  # React frontend
    "http://localhost:8000",  # Development
    "https://agrofarm.com",   # Production frontend (example)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Total-Count", "X-Process-Time"]
)

# Add request logging middleware
app.add_middleware(RequestLoggingMiddleware)

# Add error handling middleware
@app.middleware("http")
async def error_handling_middleware(request: Request, call_next):
    return await error_handler(request, call_next)

# Mount static file directory
uploads_path = Path("uploads")
uploads_path.mkdir(exist_ok=True)
app.mount("/uploads", StaticFiles(directory=uploads_path), name="uploads")

# Custom validation error handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": exc.errors(),
            "body": exc.body
        }
    )

# Include routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(product.router, prefix=settings.API_V1_STR)
app.include_router(order.router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {
        "message": "Welcome to Agro Farm E-Commerce API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }

# Startup event
@app.on_event("startup")
async def startup_event():
    # Ensure upload directories exist
    uploads_path.mkdir(exist_ok=True)
    (uploads_path / "products").mkdir(exist_ok=True)

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    pass