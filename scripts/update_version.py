#!/usr/bin/env python3
"""
Script to update the version number in the package.

Usage:
    python scripts/update_version.py 0.2.0
"""

import os
import re
import sys


def update_version(new_version):
    """Update the version in _version.py."""
    version_file = "src/agently_sdk/_version.py"
    
    with open(version_file, "r") as f:
        content = f.read()
    
    # Replace the version string
    new_content = re.sub(
        r'__version__ = "[^"]+"',
        f'__version__ = "{new_version}"',
        content
    )
    
    with open(version_file, "w") as f:
        f.write(new_content)
    
    print(f"Updated version to {new_version} in {version_file}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/update_version.py NEW_VERSION")
        sys.exit(1)
    
    new_version = sys.argv[1]
    
    # Validate version format (simple check)
    if not re.match(r"^\d+\.\d+\.\d+$", new_version):
        print("Error: Version must be in the format X.Y.Z")
        sys.exit(1)
    
    update_version(new_version) 