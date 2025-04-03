from schema_core.registry import validators


@validators.validator
def check_positive(cls, v):
    if v <= 0:
        raise ValueError("Must be positive")
    return v
