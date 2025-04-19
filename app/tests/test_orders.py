from fastapi.testclient import TestClient
from app.tests.utils import get_auth_headers

def test_create_order(client: TestClient, test_data):
    # Register a regular user
    client.post(
        "/api/auth/register",
        json={
            "email": "customer@example.com",
            "full_name": "Test Customer",
            "password": "customer123"
        }
    )
    
    # Login as customer
    headers = get_auth_headers(client, "customer@example.com", "customer123")
    
    # Get a product to order
    response = client.get("/api/products/")
    products = response.json()
    product_id = products[0]["id"]
    
    # Create order
    order_data = {
        "shipping_address": "123 Test Street",
        "contact_phone": "1234567890",
        "items": [
            {
                "product_id": product_id,
                "quantity": 2
            }
        ]
    }
    
    response = client.post(
        "/api/orders/",
        json=order_data,
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["shipping_address"] == order_data["shipping_address"]
    assert len(data["items"]) == 1
    assert data["items"][0]["quantity"] == 2

def test_list_orders(client: TestClient, test_data):
    # Register and create an order as customer
    client.post(
        "/api/auth/register",
        json={
            "email": "customer@example.com",
            "full_name": "Test Customer",
            "password": "customer123"
        }
    )
    headers = get_auth_headers(client, "customer@example.com", "customer123")
    
    # Get a product
    response = client.get("/api/products/")
    products = response.json()
    product_id = products[0]["id"]
    
    # Create order
    order_data = {
        "shipping_address": "123 Test Street",
        "contact_phone": "1234567890",
        "items": [{"product_id": product_id, "quantity": 1}]
    }
    client.post("/api/orders/", json=order_data, headers=headers)
    
    # List orders
    response = client.get("/api/orders/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["shipping_address"] == order_data["shipping_address"]

def test_cancel_order(client: TestClient, test_data):
    # Register and create an order as customer
    client.post(
        "/api/auth/register",
        json={
            "email": "customer@example.com",
            "full_name": "Test Customer",
            "password": "customer123"
        }
    )
    headers = get_auth_headers(client, "customer@example.com", "customer123")
    
    # Get a product
    response = client.get("/api/products/")
    products = response.json()
    product_id = products[0]["id"]
    initial_quantity = products[0]["stock_quantity"]
    
    # Create order
    order_data = {
        "shipping_address": "123 Test Street",
        "contact_phone": "1234567890",
        "items": [{"product_id": product_id, "quantity": 2}]
    }
    response = client.post("/api/orders/", json=order_data, headers=headers)
    order_id = response.json()["id"]
    
    # Cancel order
    response = client.post(f"/api/orders/{order_id}/cancel", headers=headers)
    assert response.status_code == 200
    
    # Verify stock is restored
    response = client.get(f"/api/products/{product_id}")
    assert response.json()["stock_quantity"] == initial_quantity