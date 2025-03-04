from app.error_handlers.bases import ErrorHandler
from .custom_errors import AppValidationError
from .handler import validation_error_handler


ValidationErrorHandler = ErrorHandler(
    function=validation_error_handler, exception_class=AppValidationError
)
