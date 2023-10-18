def warn_if_detached(func):
    """ Warn if self / cls is detached. """
    @wraps(func)
    def wrapped(this, *args, **kwargs):
        # Check for _detached in __dict__ instead of using hasattr
        # to avoid infinite loop in __getattr__
        if '_detached' in this.__dict__ and this._detached:
            warnings.warn('here')
        return func(this, *args, **kwargs)
    return wrapped