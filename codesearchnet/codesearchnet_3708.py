def _pop_none(self, kwargs):
        """Remove default values (anything where the value is None). click is unfortunately bad at the way it
        sends through unspecified defaults."""
        for key, value in copy(kwargs).items():
            # options with multiple=True return a tuple
            if value is None or value == ():
                kwargs.pop(key)
            if hasattr(value, 'read'):
                kwargs[key] = value.read()