from typing import Callable, Type


class ErrorHandler:

    def __init__(self, function: Callable, exception_class: Type[Exception]):
        self.function = function
        self.exception_class = exception_class
