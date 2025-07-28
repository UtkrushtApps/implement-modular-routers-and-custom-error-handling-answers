from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

class CustomAPIException(Exception):
    def __init__(self, status_code: int = 400, detail: str = "Something went wrong.", code: str = "error"):
        self.status_code = status_code
        self.detail = detail
        self.code = code

async def custom_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, CustomAPIException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": {
                    "message": exc.detail,
                    "code": exc.code
                }
            }
        )
    else:
        # Unknown/unexpected error
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": {
                    "message": "An unexpected error occurred.",
                    "code": "internal_error"
                }
            }
        )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # FastAPI validation errors for input
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": {
                "message": "Validation failed.",
                "code": "validation_error",
                "details": exc.errors()
            }
        }
    )
