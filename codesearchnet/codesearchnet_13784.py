def parse_all(self):
        """Parse the __all__ definition in a module."""
        assert self.current.value == "__all__"
        self.consume(tk.NAME)
        if self.current.value != "=":
            raise AllError("Could not evaluate contents of __all__. ")
        self.consume(tk.OP)
        if self.current.value not in "([":
            raise AllError("Could not evaluate contents of __all__. ")
        self.consume(tk.OP)

        self.all = []
        all_content = "("
        while self.current.kind != tk.OP or self.current.value not in ")]":
            if self.current.kind in (tk.NL, tk.COMMENT):
                pass
            elif self.current.kind == tk.STRING or self.current.value == ",":
                all_content += self.current.value
            else:
                raise AllError(
                    "Unexpected token kind in  __all__: {!r}. ".format(
                        self.current.kind
                    )
                )
            self.stream.move()
        self.consume(tk.OP)
        all_content += ")"
        try:
            self.all = eval(all_content, {})
        except BaseException as e:
            raise AllError(
                "Could not evaluate contents of __all__."
                "\bThe value was {}. The exception was:\n{}".format(all_content, e)
            )