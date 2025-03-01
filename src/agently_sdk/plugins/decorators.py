"""
Decorators for Agently plugins.

This module provides the kernel_function decorator for use in Agently plugins.
"""

import functools
from typing import Any, Callable, Optional, TypeVar, cast

F = TypeVar("F", bound=Callable[..., Any])


def kernel_function(
    func: Optional[F] = None,
    *,
    description: Optional[str] = None,
    name: Optional[str] = None,
    input_description: Optional[str] = None,
) -> Any:
    """
    Decorator for functions that should be exposed as kernel functions.

    This can be used with or without arguments:

    @kernel_function
    def my_func(): ...

    or

    @kernel_function(description="My function")
    def my_func(): ...

    Args:
        func: The function to decorate (when used without arguments)
        description: The description of the function
        name: The name of the function (defaults to the function name)
        input_description: The description of the input parameter

    Returns:
        The decorated function
    """
    # Handle the case where decorator is used without arguments
    if func is not None:

        @functools.wraps(func)
        def direct_wrapper(*args: Any, **kwargs: Any) -> Any:
            return func(*args, **kwargs)

        direct_wrapper._is_kernel_function = True  # type: ignore
        direct_wrapper._description = description  # type: ignore
        direct_wrapper._name = name  # type: ignore
        direct_wrapper._input_description = input_description  # type: ignore

        return cast(F, direct_wrapper)

    # Handle the case where decorator is used with arguments
    def decorator(inner_func: F) -> F:
        @functools.wraps(inner_func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return inner_func(*args, **kwargs)

        wrapper._is_kernel_function = True  # type: ignore
        wrapper._description = description  # type: ignore
        wrapper._name = name  # type: ignore
        wrapper._input_description = input_description  # type: ignore

        return cast(F, wrapper)

    return decorator


__all__ = ["kernel_function"]
