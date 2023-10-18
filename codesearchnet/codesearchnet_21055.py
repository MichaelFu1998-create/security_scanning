def current(self):
        """Returns the current (token, position) or (EndOfFile, EndOfFile)"""
        if self.index >= self.len:
            self._fill((self.index - self.len) + 1)
        return self.index < self.len and self.buffer[self.index] or (EndOfFile, EndOfFile)