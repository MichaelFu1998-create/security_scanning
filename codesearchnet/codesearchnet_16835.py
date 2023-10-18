def has_status(method=None, status='draft'):
    """Check that deposit has a defined status (default: draft).

    :param method: Function executed if record has a defined status.
        (Default: ``None``)
    :param status: Defined status to check. (Default: ``'draft'``)
    """
    if method is None:
        return partial(has_status, status=status)

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Check current deposit status."""
        if status != self.status:
            raise PIDInvalidAction()

        return method(self, *args, **kwargs)
    return wrapper