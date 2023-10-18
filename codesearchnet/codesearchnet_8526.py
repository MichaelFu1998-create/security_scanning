def when_called_with(self, *some_args, **some_kwargs):
        """Asserts the val callable when invoked with the given args and kwargs raises the expected exception."""
        if not self.expected:
            raise TypeError('expected exception not set, raises() must be called first')
        try:
            self.val(*some_args, **some_kwargs)
        except BaseException as e:
            if issubclass(type(e), self.expected):
                # chain on with exception message as val
                return AssertionBuilder(str(e), self.description, self.kind)
            else:
                # got exception, but wrong type, so raise
                self._err('Expected <%s> to raise <%s> when called with (%s), but raised <%s>.' % (
                    self.val.__name__,
                    self.expected.__name__,
                    self._fmt_args_kwargs(*some_args, **some_kwargs),
                    type(e).__name__))

        # didn't fail as expected, so raise
        self._err('Expected <%s> to raise <%s> when called with (%s).' % (
            self.val.__name__,
            self.expected.__name__,
            self._fmt_args_kwargs(*some_args, **some_kwargs)))