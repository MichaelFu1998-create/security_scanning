def ensure_str(value):
    """
    Ensure value is string.
    """
    if isinstance(value, six.string_types):
        return value
    else:
        return six.text_type(value)