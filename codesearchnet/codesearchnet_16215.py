def vformat(self, format_string, args, kwargs):
        """Clear used and unused dicts before each formatting."""
        self._used_kwargs = {}
        self._unused_kwargs = {}
        return super(MemorizeFormatter, self).vformat(format_string, args, kwargs)