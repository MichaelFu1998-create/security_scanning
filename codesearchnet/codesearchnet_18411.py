def get_separator(self, i):
        """Return the separator that preceding format i, or '' for i == 0."""
        return i and self.separator[min(i - 1, len(self.separator) - 1)] or ''