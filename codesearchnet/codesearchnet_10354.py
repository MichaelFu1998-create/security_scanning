def _combine_arglist(self, args, kwargs):
        """Combine the default values and the supplied values."""
        _args = self.args + args
        _kwargs = self.kwargs.copy()
        _kwargs.update(kwargs)
        return _args, _kwargs