"""
Base Plugin class for Agently plugins.
"""

import inspect
from typing import Any, Callable, Dict, List, Mapping, Optional, Type, get_type_hints

from agently_sdk.plugins.variables import PluginVariable  # Adjust import path as needed


class Plugin:
    """
    Base class for all Agently plugins.

    Plugins are classes that provide functionality to Agently agents through
    methods decorated with @kernel_function from semantic_kernel.functions.

    Example:
        ```python
        from agently_sdk.plugins import Plugin, PluginVariable, kernel_function

        class HelloPlugin(Plugin):
            # A simple greeting plugin

            name = "hello_plugin"
            description = "Provides greeting functionality"

            default_name = PluginVariable(
                name="default_name",
                description="Default name to use in greetings",
                default_value="World"
            )

            @kernel_function
            def greet(self, name: Optional[str] = None) -> str:
                # Greet someone with a friendly message.
                #
                # Args:
                #     name: The name to greet. If not provided, uses the default_name.
                #
                # Returns:
                #     A greeting message.

                name_to_use = name or self.default_name
                return f"Hello, {name_to_use}!"
        ```
    """

    name: str
    description: str

    def __init__(self, **kwargs: Any) -> None:
        """
        Initialize the plugin with configuration variables.

        Args:
            **kwargs: Configuration values for plugin variables.
        """
        # Set plugin variables from kwargs
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def get_kernel_functions(self) -> Dict[str, Callable]:
        """
        Get all methods in this class decorated with @kernel_function.

        The @kernel_function decorator from semantic_kernel.functions adds
        an attribute _is_kernel_function to the method, which we use to
        identify kernel functions.

        Returns:
            Dict[str, Callable]: A dictionary mapping function names to function objects.
        """
        result: dict[str, Callable[..., Any]] = {}

        for name, method in inspect.getmembers(self, inspect.ismethod):
            # Skip private methods
            if name.startswith("_"):
                continue

            # Check if this method has been decorated with @kernel_function
            if hasattr(method, "_is_kernel_function") and method._is_kernel_function:
                result[name] = method

        return result

    @classmethod
    def get_plugin_variables(cls) -> Dict[str, "PluginVariable"]:
        """
        Get all PluginVariable instances defined in this class.

        Returns:
            Dict[str, PluginVariable]: A dictionary mapping variable names to PluginVariable objects.
        """
        result = {}

        for name, value in inspect.getmembers(cls):
            # Skip private attributes and methods
            if name.startswith("_"):
                continue

            # Check if this is a PluginVariable
            if isinstance(value, PluginVariable):
                result[name] = value

        return result
