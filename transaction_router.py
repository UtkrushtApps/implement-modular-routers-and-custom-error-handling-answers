from fastapi import APIRouter, Request, BackgroundTasks, HTTPException, status
from fastapi.responses import JSONResponse
import time
from transaction_logger import log_audit_async
from error_handlers import CustomAPIException

router = APIRouter()

@router.post("/process")
async def process_transaction(request: Request, background_tasks: BackgroundTasks):
    start_time = time.perf_counter()
    request_body = await request.json()
    # This simulates some transaction logic; raise errors for demonstration if needed
    try:
        if not all(k in request_body for k in ("amount", "from_account", "to_account")):
            raise CustomAPIException(
                status_code=422,
                detail="Missing required transaction fields.",
                code="missing_fields"
            )
        amount = float(request_body["amount"])
        if amount <= 0:
            raise CustomAPIException(
                status_code=400,
                detail="Transaction amount must be positive.",
                code="invalid_amount"
            )
        # Simulate processing (no sleep!)
        response_data = {
            "transaction_id": "txn-{}".format(int(time.time() * 1000)),
            "status": "processed",
            "amount": amount,
            "from_account": request_body["from_account"],
            "to_account": request_body["to_account"]
        }
        status_code = 200
        error = None
    except CustomAPIException as ce:
        status_code = ce.status_code
        response_data = {"error": ce.detail, "code": ce.code}
        error = ce
    except Exception as e:
        status_code = 500
        response_data = {"error": "Internal Server Error", "code": "internal_error"}
        error = e
    duration = round((time.perf_counter() - start_time) * 1000, 2)  # in ms
    # Asynchronous background audit logging
    background_tasks.add_task(
        log_audit_async,
        request.method,
        str(request.url),
        request_body,
        response_data,
        duration,
        status_code,
        error,
    )
    if error:
        # Propagate structured errors
        if isinstance(error, CustomAPIException):
            raise error
        else:
            raise CustomAPIException(status_code=500, detail="Internal Server Error", code="internal_error")
    return response_data
