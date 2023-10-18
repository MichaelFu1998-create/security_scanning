def add(self, string, start, end, line):
        """ Add lines to the block.
        """
        if string.strip():
            # Only add if not entirely whitespace.
            self.start_lineno = min(self.start_lineno, start[0])
            self.end_lineno = max(self.end_lineno, end[0])