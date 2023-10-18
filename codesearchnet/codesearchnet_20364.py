def ilike_helper(default):
    """Helper function that performs an `ilike` query if a string value
    is passed, otherwise the normal default operation."""
    @functools.wraps(default)
    def wrapped(x, y):
        # String values should use ILIKE queries.
        if isinstance(y, six.string_types) and not isinstance(x.type, sa.Enum):
            return x.ilike("%" + y + "%")
        else:
            return default(x, y)
    return wrapped