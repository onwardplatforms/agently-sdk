"""
Decorators for Agently plugins.

This module re-exports the kernel_function decorator from semantic_kernel.functions
for use in Agently plugins.
"""

from semantic_kernel.functions import kernel_function

__all__ = ["kernel_function"] 