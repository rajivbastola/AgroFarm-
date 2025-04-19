from fastapi.testclient import TestClient
from app.tests.utils import get_auth_headers
from app.models.product import ProductCategory

def test_list_products(client: TestClient, test_data):
    response = client.get("/api/products/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert "name" in data[0]
    assert "price" in data[0]

def test_create_product(client: TestClient, test_data):
    # Login as admin
    headers = get_auth_headers(client, "admin@agrofarm.com", "admin123")
    
    product_data = {
        "name": "Test Product",
        "description": "Test Description",
        "price": 9.99,
        "stock_quantity": 50,
        "category": "VEGETABLES",
        "unit": "kg"
    }
    
    response = client.post(
        "/api/products/",
        json=product_data,
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == product_data["name"]
    assert data["price"] == product_data["price"]

def test_create_product_unauthorized(client: TestClient, test_data):
    product_data = {
        "name": "Test Product",
        "description": "Test Description",
        "price": 9.99,
        "stock_quantity": 50,
        "category": "VEGETABLES",
        "unit": "kg"
    }
    
    response = client.post("/api/products/", json=product_data)
    assert response.status_code == 401

def test_update_product(client: TestClient, test_data):
    # Login as admin
    headers = get_auth_headers(client, "admin@agrofarm.com", "admin123")
    
    # First get a product
    response = client.get("/api/products/")
    products = response.json()
    product_id = products[0]["id"]
    
    # Update the product
    update_data = {
        "name": "Updated Product",
        "price": 19.99
    }
    
    response = client.put(
        f"/api/products/{product_id}",
        json=update_data,
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["price"] == update_data["price"]

def test_delete_product(client: TestClient, test_data):
    # Login as admin
    headers = get_auth_headers(client, "admin@agrofarm.com", "admin123")
    
    # First get a product
    response = client.get("/api/products/")
    products = response.json()
    product_id = products[0]["id"]
    
    # Delete the product
    response = client.delete(
        f"/api/products/{product_id}",
        headers=headers
    )
    assert response.status_code == 200
    
    # Verify product is deleted
    response = client.get(f"/api/products/{product_id}")
    assert response.status_code == 404