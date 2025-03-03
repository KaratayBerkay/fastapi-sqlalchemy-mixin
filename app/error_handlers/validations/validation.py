from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi import status

from app.error_handlers.validations.custom_errors import AppValidationError


def validation_error_handler(request: Request, exc: AppValidationError):
    print("exc", exc)
    print("path", request.url.path)
    route_path = request.url.path
    if not exc.route:
        exc.route = route_path

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"message": f"Validation error {str(route_path)}", "error": str(exc)},
    )
