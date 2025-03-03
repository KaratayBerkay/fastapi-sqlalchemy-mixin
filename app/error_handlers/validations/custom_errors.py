from pydantic import ValidationError


class AppBaseException(Exception):
    """Base class for all application-specific exceptions."""

    pass


class AppValidationError(AppBaseException, ValidationError):

    def __init__(self, *args, route):
        super().__init__(*args)
        self.route = route

    def __str__(self):
        return f"Validation error in {self.route}"

    def __repr__(self):
        return f"Validation error in {self.route}"
