def _is_simple_numeric(data):
    """Test if a list contains simple numeric data."""
    for item in data:
        if isinstance(item, set):
            item = list(item)
        if isinstance(item, list):
            if not _is_simple_numeric(item):
                return False
        elif not isinstance(item, (int, float, complex)):
            return False
    return True