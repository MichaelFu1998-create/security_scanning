def leapfrog(self, kind, value=None):
        """Skip tokens in the stream until a certain token kind is reached.

        If `value` is specified, tokens whose values are different will also
        be skipped.
        """
        while self.current is not None:
            if self.current.kind == kind and (
                value is None or self.current.value == value
            ):
                self.consume(kind)
                return
            self.stream.move()