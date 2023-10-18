def split_elements(value):
    """Split a string with comma or space-separated elements into a list."""
    items = [v.strip() for v in value.split(',')]
    if len(items) == 1:
        items = value.split()
    return items