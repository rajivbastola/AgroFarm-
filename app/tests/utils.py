from fastapi.testclient import TestClient

def get_auth_headers(client: TestClient, email: str, password: str) -> dict:
    response = client.post(
        "/api/auth/login",
        data={
            "username": email,
            "password": password
        }
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}