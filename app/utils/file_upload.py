import os
from pathlib import Path
from fastapi import UploadFile
from PIL import Image
from uuid import uuid4
import aiofiles
from loguru import logger

# Configure upload paths
UPLOAD_DIR = Path("uploads")
PRODUCT_IMAGES_DIR = UPLOAD_DIR / "products"

# Create directories if they don't exist
PRODUCT_IMAGES_DIR.mkdir(parents=True, exist_ok=True)

# Allowed image extensions
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

# Image size limits
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB
MAX_DIMENSION = 2000  # Maximum width/height in pixels

async def save_upload_file(
    upload_file: UploadFile,
    directory: Path = PRODUCT_IMAGES_DIR
) -> str:
    """Save uploaded file and return the file path"""
    # Validate file size
    content = await upload_file.read()
    if len(content) > MAX_IMAGE_SIZE:
        raise ValueError(f"File size exceeds maximum limit of {MAX_IMAGE_SIZE/1024/1024}MB")
    
    # Validate file extension
    file_ext = Path(upload_file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"File type not allowed. Supported types: {', '.join(ALLOWED_EXTENSIONS)}")
    
    # Generate unique filename
    unique_filename = f"{uuid4()}{file_ext}"
    file_path = directory / unique_filename
    
    try:
        # Save original file
        async with aiofiles.open(file_path, "wb") as f:
            await f.write(content)
        
        # Process image
        await process_image(file_path)
        
        return str(file_path.relative_to(UPLOAD_DIR))
    
    except Exception as e:
        # Clean up file if there was an error
        if file_path.exists():
            file_path.unlink()
        logger.error(f"Error saving file: {str(e)}")
        raise

async def process_image(file_path: Path) -> None:
    """Process and optimize uploaded image"""
    try:
        with Image.open(file_path) as img:
            # Convert RGBA to RGB if needed
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            
            # Resize if image is too large
            if img.width > MAX_DIMENSION or img.height > MAX_DIMENSION:
                ratio = min(MAX_DIMENSION/img.width, MAX_DIMENSION/img.height)
                new_size = (int(img.width * ratio), int(img.height * ratio))
                img = img.resize(new_size, Image.Resampling.LANCZOS)
            
            # Optimize and save
            img.save(
                file_path,
                optimize=True,
                quality=85  # Good balance between quality and file size
            )
    
    except Exception as e:
        logger.error(f"Error processing image {file_path}: {str(e)}")
        raise

async def delete_file(file_path: str) -> bool:
    """Delete a file from the uploads directory"""
    try:
        full_path = UPLOAD_DIR / file_path
        if full_path.exists():
            full_path.unlink()
            return True
        return False
    except Exception as e:
        logger.error(f"Error deleting file {file_path}: {str(e)}")
        return False

def get_file_url(file_path: str) -> str:
    """Convert file path to URL"""
    return f"/uploads/{file_path}"