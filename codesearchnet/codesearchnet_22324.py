def one(func, n=0):
    """
    Create a callable that applies ``func`` to a value in a sequence.

    If the value is not a sequence or is an empty sequence then ``None`` is
    returned.

    :type  func: `callable`
    :param func: Callable to be applied to each result.

    :type  n: `int`
    :param n: Index of the value to apply ``func`` to.
    """
    def _one(result):
        if _isSequenceTypeNotText(result) and len(result) > n:
            return func(result[n])
        return None
    return maybe(_one)