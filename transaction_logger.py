import threading

audit_logs = []  # this simulates in-memory log storage (not prod safe)
_audit_log_lock = threading.Lock()

def log_audit_async(method, url, request_data, response_data, duration_ms, status_code, error=None):
    # Run in FastAPI BackgroundTasks (i.e. not blocking request lifecycle)
    log_entry = {
        "method": method,
        "url": url,
        "request": request_data,
        "response": response_data,
        "duration_ms": duration_ms,
        "status_code": status_code,
        "error": str(error) if error else None
    }
    with _audit_log_lock:
        audit_logs.append(log_entry)
