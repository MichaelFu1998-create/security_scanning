def _parse_from_import_names(self, is_future_import):
        """Parse the 'y' part in a 'from x import y' statement."""
        if self.current.value == "(":
            self.consume(tk.OP)
            expected_end_kinds = (tk.OP,)
        else:
            expected_end_kinds = (tk.NEWLINE, tk.ENDMARKER)
        while self.current.kind not in expected_end_kinds and not (
            self.current.kind == tk.OP and self.current.value == ";"
        ):
            if self.current.kind != tk.NAME:
                self.stream.move()
                continue
            self.log.debug(
                "parsing import, token is %r (%s)",
                self.current.kind,
                self.current.value,
            )
            if is_future_import:
                self.log.debug("found future import: %s", self.current.value)
                self.future_imports.add(self.current.value)
            self.consume(tk.NAME)
            self.log.debug(
                "parsing import, token is %r (%s)",
                self.current.kind,
                self.current.value,
            )
            if self.current.kind == tk.NAME and self.current.value == "as":
                self.consume(tk.NAME)  # as
                if self.current.kind == tk.NAME:
                    self.consume(tk.NAME)  # new name, irrelevant
            if self.current.value == ",":
                self.consume(tk.OP)
            self.log.debug(
                "parsing import, token is %r (%s)",
                self.current.kind,
                self.current.value,
            )