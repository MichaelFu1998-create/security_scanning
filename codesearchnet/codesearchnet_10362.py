def _combineargs(self, *args, **kwargs):
        """Add switches as 'options' with value True to the options dict."""
        d = {arg: True for arg in args}   # switches are kwargs with value True
        d.update(kwargs)
        return d