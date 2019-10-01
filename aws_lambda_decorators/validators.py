"""Validation rules."""
import re
from schema import SchemaError


class Validator:  # noqa: pylint - too-few-public-methods
    """Validation rule to check if the given mandatory value exists."""
    ERROR_MESSAGE = "Unknown error"

    def __init__(self, error_message, condition=None):
        """
        Validates a parameter

        Args:
            error_message (str): A custom error message to output if validation fails
            condition (any): A condition to validate
        """
        self._error_message = error_message or self.ERROR_MESSAGE
        self._condition = condition

    def message(self, value=None):  # noqa: pylint - unused-argument
        """
        Gets the formatted error message for a failed mandatory check

        Args:
            value (any): The validated value

        Returns:
            The error message
        """
        return self._error_message.format(value=value, condition=self._condition)


class Mandatory(Validator):  # noqa: pylint - too-few-public-methods
    """Validation rule to check if the given mandatory value exists."""
    ERROR_MESSAGE = "Missing mandatory value"

    def __init__(self, error_message=None):
        """
        Checks if a parameter has a value

        Args:
            error_message (str): A custom error message to output if validation fails
        """
        super().__init__(error_message)

    @staticmethod
    def validate(value=None):
        """
        Check if the given mandatory value exists.

        Args:
            value (any): Value to be validated.
        """
        return value is not None and str(value)


class RegexValidator(Validator):  # noqa: pylint - too-few-public-methods
    """Validation rule to check if a value matches a regular expression."""
    ERROR_MESSAGE = "'{value}' does not conform to regular expression '{condition}'"

    def __init__(self, regex='', error_message=None):
        """
        Compile a regular expression to a regular expression pattern.

        Args:
            regex (str): Regular expression for parameter validation.
            error_message (str): A custom error message to output if validation fails
        """
        super().__init__(error_message, regex)
        self._regexp = re.compile(regex)

    def validate(self, value=None):
        """
        Check if a value adheres to the defined regular expression.

        Args:
            value (str): Value to be validated.
        """
        return self._regexp.fullmatch(value) is not None


class SchemaValidator(Validator):  # noqa: pylint - too-few-public-methods
    """Validation rule to check if a value matches a regular expression."""
    ERROR_MESSAGE = "'{value}' does not validate against schema '{condition}'"

    def __init__(self, schema, error_message=None):
        """
        Set the schema field.

        Args:
            schema (Schema): The expected schema.
            error_message (str): A custom error message to output if validation fails
        """
        super().__init__(error_message, schema)

    def validate(self, value=None):
        """
        Check if the object adheres to the defined schema.

        Args:
            value (object): Value to be validated.
        """
        try:
            return self._condition.validate(value) == value
        except SchemaError:
            return False


class Minimum(Validator):  # noqa: pylint - too-few-public-methods
    """Validation rule to check if a value is greater than a minimum value."""
    ERROR_MESSAGE = "'{value}' is less than minimum value '{condition}'"

    def __init__(self, minimum: (float, int), error_message=None):
        """
        Set the minimum value.

        Args:
            minimum (float, int): The minimum value.
            error_message (str): A custom error message to output if validation fails
        """
        super().__init__(error_message, minimum)

    def validate(self, value=None):
        """
        Check if the value is greater than the minimum.

        Args:
            value (float, int): Value to be validated.
        """
        if value is None:
            return True

        if isinstance(value, (float, int)):
            return self._condition <= value

        return False


class Maximum(Validator):  # noqa: pylint - too-few-public-methods
    """Validation rule to check if a value is less than a maximum value."""
    ERROR_MESSAGE = "'{value}' is greater than maximum value '{condition}'"

    def __init__(self, maximum: (float, int), error_message=None):
        """
        Set the maximum value.

        Args:
            maximum (float, int): The maximum value.
            error_message (str): A custom error message to output if validation fails
        """
        super().__init__(error_message, maximum)

    def validate(self, value=None):
        """
        Check if the value is less than the maximum.

        Args:
            value (float, int): Value to be validated.
        """
        if value is None:
            return True

        if isinstance(value, (float, int)):
            return self._condition >= value

        return False


class MinLength(Validator):  # noqa: pylint - too-few-public-methods
    """Validation rule to check if a string is shorter than a minimum length."""
    ERROR_MESSAGE = "'{value}' is shorter than minimum length '{condition}'"

    def __init__(self, min_length: int, error_message=None):
        """
        Set the minimum length.

        Args:
            min_length (int): The minimum length.
            error_message (str): A custom error message to output if validation fails
        """
        super().__init__(error_message, min_length)

    def validate(self, value=None):
        """
        Check if a string is shorter than the minimum length.

        Args:
            value (str): String to be validated.
        """
        if value is None:
            return True

        return len(str(value)) >= self._condition


class MaxLength(Validator):  # noqa: pylint - too-few-public-methods
    """Validation rule to check if a string is longer than a maximum length."""
    ERROR_MESSAGE = "'{value}' is longer than maximum length '{condition}'"

    def __init__(self, max_length: int, error_message=None):
        """
        Set the maximum length.

        Args:
            max_length (int): The maximum length.
            error_message (str): A custom error message to output if validation fails
        """
        super().__init__(error_message, max_length)

    def validate(self, value=None):
        """
        Check if a string is longer than the maximum length.

        Args:
            value (str): String to be validated.
        """
        if value is None:
            return True

        return len(str(value)) <= self._condition
