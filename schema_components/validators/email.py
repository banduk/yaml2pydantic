from schema_core.registry import validators


@validators.validator
def email_contains_name(cls, values):
    name, email = values.get("name"), values.get("email")
    if email and name.lower() not in email.lower():
        raise ValueError("Email must contain user's name")
    return values
