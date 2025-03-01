"""
Agently SDK - Official SDK for developing extensions for the Agently framework.

Currently focused on plugin development, with more capabilities planned for future releases.
"""

__version__ = "0.1.0"

# Import plugin-related components for convenience
from agently_sdk.plugins import Plugin, PluginVariable, kernel_function

__all__ = ["Plugin", "PluginVariable", "kernel_function"]
