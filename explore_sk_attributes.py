#!/usr/bin/env python3
"""
Script to explore the attributes added by Semantic Kernel's kernel_function decorator.
"""

try:
    from semantic_kernel.functions import kernel_function as sk_kernel_function
    
    # Create a function with SK's decorator
    @sk_kernel_function(description="Test function", name="test_func")
    def decorated_func(x: int) -> int:
        """Test function docstring."""
        return x * 2
    
    print("Attributes of a function decorated with SK's kernel_function:")
    print("-----------------------------------------------------------")
    
    # Get all attributes
    all_attrs = dir(decorated_func)
    
    # Filter out dunder methods
    sk_attrs = [attr for attr in all_attrs if not attr.startswith("__")]
    
    # Print each attribute and its value
    for attr in sorted(sk_attrs):
        try:
            value = getattr(decorated_func, attr)
            print(f"{attr}: {value}")
        except Exception as e:
            print(f"{attr}: <Error: {e}>")
    
    # Check for specific attributes we're interested in
    print("\nChecking for specific attributes:")
    print("--------------------------------")
    specific_attrs = [
        "_description",
        "_name",
        "_method",
        "_parameters",
        "_return_type",
        "_is_kernel_function",
        "__kernel_function__"
    ]
    
    for attr in specific_attrs:
        if hasattr(decorated_func, attr):
            value = getattr(decorated_func, attr)
            print(f"{attr}: {value}")
        else:
            print(f"{attr}: Not found")
    
except ImportError:
    print("Semantic Kernel is not installed.") 