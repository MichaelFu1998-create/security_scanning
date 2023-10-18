def move(self):
        """Move."""
        previous = self.current
        current = self._next_from_generator()
        self.current = None if current is None else Token(*current)
        self.line = self.current.start[0] if self.current else self.line
        self.got_logical_newline = previous.kind in self.LOGICAL_NEWLINES
        return previous