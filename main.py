from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from transaction_router import router as transaction_router
from error_handlers import CustomAPIException, custom_exception_handler, validation_exception_handler

app = FastAPI()

# Allow CORS for demonstration and local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the modular transaction router
app.include_router(transaction_router, prefix='/transaction')

# Add custom error handlers
app.add_exception_handler(CustomAPIException, custom_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, custom_exception_handler)

@app.get("/logs")
def get_logs():
    """
    Expose audit logs for demonstration/testing purposes
    """
    from transaction_logger import audit_logs
    return {"logs": audit_logs}
