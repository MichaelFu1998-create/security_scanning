def parse_docstring(self):
        """Parse a single docstring and return its value."""
        self.log.debug(
            "parsing docstring, token is %r (%s)", self.current.kind, self.current.value
        )
        while self.current.kind in (tk.COMMENT, tk.NEWLINE, tk.NL):
            self.stream.move()
            self.log.debug(
                "parsing docstring, token is %r (%s)",
                self.current.kind,
                self.current.value,
            )
        if self.current.kind == tk.STRING:
            docstring = self.current.value
            self.stream.move()
            return docstring
        return None