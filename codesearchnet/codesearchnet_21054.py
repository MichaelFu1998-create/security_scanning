def next(self):
        """Advances to and returns the next token or returns EndOfFile"""
        self.index += 1
        t = self.peek()
        if not self.depth:
            self._cut()
        return t