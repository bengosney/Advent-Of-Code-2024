# Standard Library
from collections.abc import Callable
from functools import wraps
from typing import Any

# Third Party
import pytest


def no_input_skip(f: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(f)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return f(*args, **kwargs)
        except FileNotFoundError:
            pytest.skip("Input file not found")

    return wrapper
