def check_current(self, kind=None, value=None):
        """Verify the current token is of type `kind` and equals `value`."""
        msg = textwrap.dedent(
            """
        Unexpected token at line {self.line}:
        In file: {self.filename}
        Got kind {self.current.kind!r}
        Got value {self.current.value}
        """.format(
                self=self
            )
        )
        kind_valid = self.current.kind == kind if kind else True
        value_valid = self.current.value == value if value else True
        assert kind_valid and value_valid, msg