"""
Style builder implementation for Agently SDK styles.

This module implements the StyleBuilder class which provides a fluent interface
for applying text styles.
"""

import os
from typing import Any, Dict, Optional


class StyleBuilder:
    """
    A builder for creating styled text with a fluent interface.

    This class allows style attributes to be chained as properties
    and then applied to text by calling the resulting builder.

    Examples:
        >>> from agently_sdk.styles import styles
        >>> print(styles.blue("Blue text"))
        >>> print(styles.bold.red("Bold red text"))
        >>> print(styles.underline.green.italic("Complex styling"))
    """

    # Check if colors should be disabled
    _NO_COLOR = os.environ.get("NO_COLOR", "").lower() in ("1", "true", "yes")

    # ANSI color codes
    _COLORS = {
        "black": "\033[30m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
        "bright_black": "\033[90m",
        "bright_red": "\033[91m",
        "bright_green": "\033[92m",
        "bright_yellow": "\033[93m",
        "bright_blue": "\033[94m",
        "bright_magenta": "\033[95m",
        "bright_cyan": "\033[96m",
        "bright_white": "\033[97m",
    }

    # Background colors
    _BG_COLORS = {
        "bg_black": "\033[40m",
        "bg_red": "\033[41m",
        "bg_green": "\033[42m",
        "bg_yellow": "\033[43m",
        "bg_blue": "\033[44m",
        "bg_magenta": "\033[45m",
        "bg_cyan": "\033[46m",
        "bg_white": "\033[47m",
        "bg_bright_black": "\033[100m",
        "bg_bright_red": "\033[101m",
        "bg_bright_green": "\033[102m",
        "bg_bright_yellow": "\033[103m",
        "bg_bright_blue": "\033[104m",
        "bg_bright_magenta": "\033[105m",
        "bg_bright_cyan": "\033[106m",
        "bg_bright_white": "\033[107m",
    }

    # Text formatting
    _FORMATS = {
        "bold": "\033[1m",
        "dim": "\033[2m",
        "italic": "\033[3m",
        "underline": "\033[4m",
        "blink": "\033[5m",
        "reverse": "\033[7m",
        "hidden": "\033[8m",
        "strikethrough": "\033[9m",
    }

    # Reset code
    _RESET = "\033[0m"

    def __init__(self, styles: Optional[Dict[str, str]] = None):
        """
        Initialize a StyleBuilder with optional initial styles.

        Args:
            styles: Dictionary of style attributes to apply
        """
        self._styles = styles or {}

    def __call__(self, text: str) -> str:
        """
        Apply all accumulated styles to the provided text.

        Args:
            text: The text to style

        Returns:
            Styled text with ANSI codes
        """
        if self._NO_COLOR or not self._styles:
            return text

        # Collect all style codes
        codes = []
        for style_name, _ in self._styles.items():
            if style_name in self._COLORS:
                codes.append(self._COLORS[style_name])
            elif style_name in self._BG_COLORS:
                codes.append(self._BG_COLORS[style_name])
            elif style_name in self._FORMATS:
                codes.append(self._FORMATS[style_name])

        # Apply the styles and reset at the end
        if not codes:
            return text
        return f"{''.join(codes)}{text}{self._RESET}"

    def style(self, text: str, **kwargs: Any) -> str:
        """
        Apply specified styles to text.

        This is a function-based alternative to the fluent interface.

        Args:
            text: The text to style
            **kwargs: Style attributes to apply (color, bg_color, bold, etc.)

        Returns:
            Styled text
        """
        # Create a new builder with the combined styles
        builder = StyleBuilder(self._styles.copy())

        # Apply each style
        for style_name, value in kwargs.items():
            if value and hasattr(builder, style_name):
                builder = getattr(builder, style_name)

        # Apply the styles to the text
        return builder(text)

    # Define color properties
    @property
    def black(self) -> "StyleBuilder":
        return self._add_style("black")

    @property
    def red(self) -> "StyleBuilder":
        return self._add_style("red")

    @property
    def green(self) -> "StyleBuilder":
        return self._add_style("green")

    @property
    def yellow(self) -> "StyleBuilder":
        return self._add_style("yellow")

    @property
    def blue(self) -> "StyleBuilder":
        return self._add_style("blue")

    @property
    def magenta(self) -> "StyleBuilder":
        return self._add_style("magenta")

    @property
    def cyan(self) -> "StyleBuilder":
        return self._add_style("cyan")

    @property
    def white(self) -> "StyleBuilder":
        return self._add_style("white")

    # Background color properties
    @property
    def bg_black(self) -> "StyleBuilder":
        return self._add_style("bg_black")

    @property
    def bg_red(self) -> "StyleBuilder":
        return self._add_style("bg_red")

    @property
    def bg_green(self) -> "StyleBuilder":
        return self._add_style("bg_green")

    @property
    def bg_yellow(self) -> "StyleBuilder":
        return self._add_style("bg_yellow")

    @property
    def bg_blue(self) -> "StyleBuilder":
        return self._add_style("bg_blue")

    @property
    def bg_magenta(self) -> "StyleBuilder":
        return self._add_style("bg_magenta")

    @property
    def bg_cyan(self) -> "StyleBuilder":
        return self._add_style("bg_cyan")

    @property
    def bg_white(self) -> "StyleBuilder":
        return self._add_style("bg_white")

    # Format properties
    @property
    def bold(self) -> "StyleBuilder":
        return self._add_style("bold")

    @property
    def dim(self) -> "StyleBuilder":
        return self._add_style("dim")

    @property
    def italic(self) -> "StyleBuilder":
        return self._add_style("italic")

    @property
    def underline(self) -> "StyleBuilder":
        return self._add_style("underline")

    @property
    def blink(self) -> "StyleBuilder":
        return self._add_style("blink")

    @property
    def reverse(self) -> "StyleBuilder":
        return self._add_style("reverse")

    @property
    def hidden(self) -> "StyleBuilder":
        return self._add_style("hidden")

    @property
    def strikethrough(self) -> "StyleBuilder":
        return self._add_style("strikethrough")

    # Common message type shortcuts
    def info(self, message: str) -> str:
        """Format an informational message (cyan)."""
        return self.cyan(message)

    def success(self, message: str) -> str:
        """Format a success message (green + bold)."""
        return self.green.bold(message)

    def warning(self, message: str) -> str:
        """Format a warning message (yellow)."""
        return self.yellow(message)

    def error(self, message: str) -> str:
        """Format an error message (red + bold)."""
        return self.red.bold(message)

    def debug(self, message: str) -> str:
        """Format a debug message (dim)."""
        return self.dim(message)

    def _add_style(self, style_name: str) -> "StyleBuilder":
        """
        Add a style to the builder and return a new builder.

        Args:
            style_name: The name of the style to add

        Returns:
            A new StyleBuilder with the added style
        """
        new_styles = self._styles.copy()
        new_styles[style_name] = True  # type: ignore
        return StyleBuilder(new_styles)
