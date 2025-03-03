"""
Example demonstrating the ExecutionResult functionality.

This example shows how to use the ExecutionResult feature to get detailed
information about function execution in Agently plugins.
"""

from agently_sdk.plugins import (
    Plugin, 
    PluginVariable, 
    agently_function, 
    track_function_calls,
    ExecutionResult,
    get_result
)


class FilePlugin(Plugin):
    """A plugin for file operations."""

    name = "file_plugin"
    description = "Provides file operation functionality"

    @agently_function(action="Reading file")
    def read_file(self, filename: str) -> str:
        """Read the contents of a file."""
        print(f"Reading file: {filename}")
        try:
            with open(filename, "r") as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {str(e)}"

    @agently_function(action="Writing to file")
    def write_file(self, filename: str, content: str) -> bool:
        """Write content to a file."""
        print(f"Writing to file: {filename}")
        try:
            with open(filename, "w") as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Error writing to file: {str(e)}")
            return False


def main():
    # Create a plugin instance
    plugin = FilePlugin()

    # By default, execution reporting is disabled
    result = plugin.read_file("examples/execution_result_demo.py")
    print("\nWithout function tracking:")
    print(f"Result type: {type(result)}")
    print(f"Result: {result[:50]}...")  # Show first 50 chars

    # Enable function tracking
    print("\nEnabling function tracking...")
    track_function_calls(True)

    # Now we get ExecutionResult objects
    result = plugin.read_file("examples/execution_result_demo.py")
    print("\nWith function tracking:")
    print(f"Result type: {type(result)}")
    print(f"Action: {result.action}")
    print(f"Duration: {result.metadata['duration']:.6f} seconds")
    print(f"Function name: {result.metadata['function_name']}")
    print(f"Actual value: {result.value[:50]}...")  # Show first 50 chars

    # Write a file with function tracking
    write_result = plugin.write_file("example_output.txt", "Hello, world!")
    print("\nWrite operation:")
    print(f"Action: {write_result.action}")
    print(f"Duration: {write_result.metadata['duration']:.6f} seconds")
    print(f"Success: {write_result.value}")

    # Using get_result to extract the actual result
    success = get_result(write_result)
    if success:
        print("File was written successfully!")
    else:
        print("File writing failed!")

    # Disable function tracking
    print("\nDisabling function tracking...")
    track_function_calls(False)

    # Now we get direct results again
    result = plugin.read_file("example_output.txt")
    print("\nAfter disabling function tracking:")
    print(f"Result type: {type(result)}")
    print(f"Result: {result}")


if __name__ == "__main__":
    main() 