def get_context(obj):
    """Search for a context manager"""
    try:
        return obj._contexts[-1]
    except (AttributeError, IndexError):
        pass

    try:
        return obj._model._contexts[-1]
    except (AttributeError, IndexError):
        pass

    return None