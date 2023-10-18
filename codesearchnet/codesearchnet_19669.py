def display(self):
        """
        When dealing with optgroups, ensure that the value is properly force_text'd.
        """
        if not self.is_group():
            return self._display
        return ((force_text(k), v) for k, v in self._display)