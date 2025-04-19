from typing import Any, Dict

def generate_response_schema(model_name: str) -> Dict[str, Any]:
    """Generate OpenAPI response schema for common response patterns."""
    return {
        200: {
            "description": "Successful Response",
            "content": {
                "application/json": {
                    "schema": {"$ref": f"#/components/schemas/{model_name}"}
                }
            }
        },
        401: {
            "description": "Authentication Error",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "detail": {"type": "string"}
                        }
                    }
                }
            }
        },
        403: {
            "description": "Permission Error",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "detail": {"type": "string"}
                        }
                    }
                }
            }
        },
        404: {
            "description": "Not Found Error",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "detail": {"type": "string"}
                        }
                    }
                }
            }
        },
        422: {
            "description": "Validation Error",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/HTTPValidationError"
                    }
                }
            }
        }
    }

api_tags_metadata = [
    {
        "name": "auth",
        "description": "Authentication operations including login and registration"
    },
    {
        "name": "products",
        "description": "Operations with products including listing, creation, and management"
    },
    {
        "name": "orders",
        "description": "Order management including creation, listing, and status updates"
    }
]