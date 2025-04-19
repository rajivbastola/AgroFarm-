from fastapi.testclient import TestClient

def test_register_user(client: TestClient):
    response = client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "full_name": "Test User",
            "password": "testpass123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["full_name"] == "Test User"
    assert "id" in data

def test_login_user(client: TestClient, test_data):
    # First register a user
    client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "full_name": "Test User",
            "password": "testpass123"
        }
    )
    
    # Then try to login
    response = client.post(
        "/api/auth/login",
        data={
            "username": "test@example.com",
            "password": "testpass123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password(client: TestClient, test_data):
    # First register a user
    client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "full_name": "Test User",
            "password": "testpass123"
        }
    )
    
    # Try to login with wrong password
    response = client.post(
        "/api/auth/login",
        data={
            "username": "test@example.com",
            "password": "wrongpass"
        }
    )
    assert response.status_code == 401