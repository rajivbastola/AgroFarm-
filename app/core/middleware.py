from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from app.core.exceptions import AgroFarmException

async def error_handler(request: Request, call_next):
    try:
        return await call_next(request)
    except AgroFarmException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={"detail": e.detail}
        )
    except SQLAlchemyError as e:
        return JSONResponse(
            status_code=500,
            content={"detail": "Database error occurred"}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )