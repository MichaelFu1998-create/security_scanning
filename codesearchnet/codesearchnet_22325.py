def many(func):
    """
    Create a callable that applies ``func`` to every value in a sequence.

    If the value is not a sequence then an empty list is returned.

    :type  func: `callable`
    :param func: Callable to be applied to the first result.
    """
    def _many(result):
        if _isSequenceTypeNotText(result):
            return map(func, result)
        return []
    return maybe(_many, default=[])