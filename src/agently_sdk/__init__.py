"""
Agently SDK - Official SDK for developing extensions for the Agently framework.

Currently focused on plugin development, with more capabilities planned for future releases.
"""

# Import plugin-related components for convenience
from agently_sdk.plugins import (
    Plugin,
    PluginVariable,
    VariableValidation,
    agently_function,
    kernel_function,
)

# Import styles for convenience
from agently_sdk.styles import styles

__all__ = [
    # Plugin components
    "Plugin",
    "PluginVariable",
    "VariableValidation",
    "agently_function",
    "kernel_function",
    # Styles
    "styles",
]
