from typing import Callable, Type


class ErrorHandler:
    function: Callable
    exception_class: Type[Exception]
