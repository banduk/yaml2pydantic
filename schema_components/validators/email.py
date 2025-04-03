"""Email validation functions."""

from schema_core.registry import validators


@validators.validator
def email_contains_name(cls, values):
    """Validate that the email contains the user's name.

    This validator ensures that if an email is provided, it contains
    the user's name (case-insensitive).

    Args:
    ----
        cls: The model class (unused)
        values: Dictionary containing model values

    Returns:
    -------
        The validated values

    Raises:
    ------
        ValueError: If the email doesn't contain the user's name

    """
    name, email = values.get("name"), values.get("email")
    if email and name.lower() not in email.lower():
        raise ValueError("Email must contain user's name")
    return values
