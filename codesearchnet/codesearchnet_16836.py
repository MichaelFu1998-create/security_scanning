def preserve(method=None, result=True, fields=None):
    """Preserve fields in deposit.

    :param method: Function to execute. (Default: ``None``)
    :param result: If `True` returns the result of method execution,
        otherwise `self`. (Default: ``True``)
    :param fields: List of fields to preserve (default: ``('_deposit',)``).
    """
    if method is None:
        return partial(preserve, result=result, fields=fields)

    fields = fields or ('_deposit', )

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Check current deposit status."""
        data = {field: self[field] for field in fields if field in self}
        result_ = method(self, *args, **kwargs)
        replace = result_ if result else self
        for field in data:
            replace[field] = data[field]
        return result_
    return wrapper