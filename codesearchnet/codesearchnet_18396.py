def _wraptext(self, text, indent=0, width=0):
        """Shorthand for '\n'.join(self._wrap(par, indent, width) for par in text)."""
        return '\n'.join(self._wrap(par, indent, width) for par in text)