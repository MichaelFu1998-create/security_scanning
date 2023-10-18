def parse_definitions(self, class_, all=False):
        """Parse multiple definitions and yield them."""
        while self.current is not None:
            self.log.debug(
                "parsing definition list, current token is %r (%s)",
                self.current.kind,
                self.current.value,
            )
            self.log.debug("got_newline: %s", self.stream.got_logical_newline)
            if all and self.current.value == "__all__":
                self.parse_all()
            elif (
                self.current.kind == tk.OP
                and self.current.value == "@"
                and self.stream.got_logical_newline
            ):
                self.consume(tk.OP)
                self.parse_decorators()
            elif self.current.value in ["def", "class"]:
                yield self.parse_definition(class_._nest(self.current.value))
            elif self.current.kind == tk.INDENT:
                self.consume(tk.INDENT)
                for definition in self.parse_definitions(class_):
                    yield definition
            elif self.current.kind == tk.DEDENT:
                self.consume(tk.DEDENT)
                return
            elif self.current.value == "from":
                self.parse_from_import_statement()
            else:
                self.stream.move()