from typing import List
from fastapi import FastAPI

from .bases import ErrorHandler


class ErrorHandlerRegisterController:

    def __init__(self, app: FastAPI, exception_classes: List[ErrorHandler]):
        self.app = app
        self.exception_classes = exception_classes

    def register_error_handlers(self):
        for exception_class in self.exception_classes:
            print('Exception name:', exception_class)
            self.app.add_exception_handler(exception_class.exception_class, exception_class.function)
