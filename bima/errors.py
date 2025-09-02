from rest_framework.views import exception_handler

def exception_handler_json(exc, context):
    resp = exception_handler(exc, context)
    if not resp:
        return resp
    raw = resp.data

    if isinstance(raw, dict):
        # DRF ValidationError -> {field: [msg]}
        details = {k: (v[0] if isinstance(v, list) else v) for k, v in raw.items()}
        message = "; ".join([f"{k}: {v}" for k, v in details.items()])
    elif isinstance(raw, list):
        details = {}
        message = ", ".join(map(str, raw))
    else:
        details, message = {}, str(raw)

    resp.data = {"error": {"code": resp.status_code, "message": message, "details": details}}
    return resp
