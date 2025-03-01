"""
Tests for the PluginVariable class.
"""

import pytest

from agently_sdk.plugins.variables import PluginVariable


def test_plugin_variable_initialization():
    """Test that a plugin variable can be initialized with various options."""
    # Basic initialization
    var = PluginVariable(name="test_var", description="A test variable", default="default")
    assert var.name == "test_var"
    assert var.description == "A test variable"
    assert var.default_value == "default"
    assert not var.required

    # With required=True
    var = PluginVariable(name="required_var", description="A required variable", required=True)
    assert var.required
    assert var.default_value is None

    # With choices
    var = PluginVariable(
        name="choice_var",
        description="A variable with choices",
        choices=["option1", "option2", "option3"],
        default="option1",
    )
    assert var.choices == ["option1", "option2", "option3"]
    assert var.default_value == "option1"

    # With validator
    def is_positive(x):
        return x > 0

    var = PluginVariable(
        name="validated_var",
        description="A variable with a validator",
        validator=is_positive,
        default=10,
    )
    assert var.validator is is_positive
    assert var.default_value == 10


def test_plugin_variable_validation():
    """Test that plugin variables validate values correctly."""
    # Type validation
    var = PluginVariable(name="int_var", description="An integer variable", type=int, default=42)

    assert var.validate(100)  # Should pass

    with pytest.raises(ValueError):
        var.validate("not an int")  # Should fail

    # Choices validation
    var = PluginVariable(
        name="choice_var",
        description="A variable with choices",
        choices=["red", "green", "blue"],
        default="red",
    )

    assert var.validate("red")  # Should pass
    assert var.validate("green")  # Should pass

    with pytest.raises(ValueError):
        var.validate("yellow")  # Should fail

    # Custom validator
    var = PluginVariable(
        name="even_var",
        description="Must be an even number",
        validator=lambda x: x % 2 == 0,
        default=2,
    )

    assert var.validate(4)  # Should pass
    assert var.validate(0)  # Should pass

    with pytest.raises(ValueError):
        var.validate(3)  # Should fail

    # Required validation
    var = PluginVariable(
        name="required_var",
        description="A required variable",
        required=True,
        default="default",
    )

    assert var.validate("value")  # Should pass

    with pytest.raises(ValueError):
        var.validate(None)  # Should fail


def test_plugin_variable_descriptor():
    """Test that plugin variables work as descriptors."""

    class TestClass:
        var = PluginVariable(name="test_var", description="A test variable", default="default")

    obj = TestClass()

    # Get the default value
    assert obj.var == "default"

    # Set a new value
    obj.var = "new value"
    assert obj.var == "new value"

    # Try to set an invalid value (if we had validation)
    var_with_validation = PluginVariable(
        name="validated_var", description="A validated variable", type=int, default=1
    )

    # Replace the descriptor
    TestClass.var = var_with_validation

    obj2 = TestClass()
    assert obj2.var == 1

    obj2.var = 42
    assert obj2.var == 42

    with pytest.raises(ValueError):
        obj2.var = "not an int"


def test_to_dict():
    """Test that to_dict returns the expected dictionary."""
    var = PluginVariable(
        name="test_var",
        description="A test variable",
        default="default",
        required=True,
        choices=["default", "option1", "option2"],
        type=str,
    )

    result = var.to_dict()

    assert result["name"] == "test_var"
    assert result["description"] == "A test variable"
    assert result["default"] == "default"
    assert result["required"] is True
    assert result["choices"] == ["default", "option1", "option2"]
    assert result["type"] == "str"


def test_plugin_variable_init():
    var = PluginVariable(name="test", description="Test variable", default="default")
    assert var.name == "test"
    assert var.description == "Test variable"
    assert var.default_value == "default"
    assert not var.required

    var = PluginVariable(name="test", description="Test variable")
    assert var.default_value is None


def test_plugin_variable_with_choices():
    var = PluginVariable(
        name="test",
        description="Test variable",
        choices=["option1", "option2"],
        default="option1",
    )
    assert var.choices == ["option1", "option2"]
    assert var.default_value == "option1"

    # Test validation with choices
    var.validate("option1")  # Should not raise
    var.validate("option2")  # Should not raise
    with pytest.raises(ValueError):
        var.validate("option3")  # Should raise ValueError


def test_plugin_variable_with_type():
    var = PluginVariable(name="test", description="Test variable", type=int, default=10)
    assert var.value_type == int
    assert var.default_value == 10

    # Test validation with type
    var.validate(20)  # Should not raise
    with pytest.raises(ValueError):
        var.validate("not an int")  # Should raise ValueError
