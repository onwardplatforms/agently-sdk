"""
Styles module for Agently SDK.

This module provides a flexible, intuitive styling system for terminal output.
The main export is the 'styles' object which provides a fluent interface for styling text.
"""

from agently_sdk.styles.builder import StyleBuilder

# Create the main styles instance that will be imported by users
styles = StyleBuilder()

# Export the primary interface - just the styles object
__all__ = ["styles"]
