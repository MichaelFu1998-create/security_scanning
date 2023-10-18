def _censor_with(x, range, value=None):
    """
    Censor any values outside of range with ``None``
    """
    return [val if range[0] <= val <= range[1] else value
            for val in x]