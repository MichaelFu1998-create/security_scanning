def sync_required(func):
    """Decorate methods when synchronizing repository is required."""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self._keepSynchronized:
            r = func(self, *args, **kwargs)
        else:
            state = self._load_state()
            #print("----------->  ",state, self.state)
            if state is None:
                r = func(self, *args, **kwargs)
            elif state == self.state:
                r = func(self, *args, **kwargs)
            else:
                warnings.warn("Repository at '%s' is out of date. Need to load it again to avoid conflict."%self.path)
                r = None
        return r
    return wrapper