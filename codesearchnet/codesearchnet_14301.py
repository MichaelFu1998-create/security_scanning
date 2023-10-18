def clean_undefined(obj):
    """
    Convert Undefined array entries to None (null)
    """
    if isinstance(obj, list):
        return [
            None if isinstance(item, Undefined) else item
            for item in obj
        ]
    if isinstance(obj, dict):
        for key in obj:
            obj[key] = clean_undefined(obj[key])
    return obj