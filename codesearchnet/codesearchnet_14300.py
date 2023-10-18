def get_value(obj, key, default=None):
    """
    Mimic JavaScript Object/Array behavior by allowing access to nonexistent
    indexes.
    """
    if isinstance(obj, dict):
        return obj.get(key, default)
    elif isinstance(obj, list):
        try:
            return obj[key]
        except IndexError:
            return default