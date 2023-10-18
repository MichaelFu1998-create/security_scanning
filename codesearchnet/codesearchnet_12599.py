def run_matcher(self, subject, *expected, **kw):
        """
        Runs the operator matcher test function.
        """
        # Update assertion expectation
        self.expected = expected

        _args = (subject,)
        if self.kind == OperatorTypes.MATCHER:
            _args += expected

        try:
            result = self.match(*_args, **kw)
        except Exception as error:
            return self._make_error(error=error)

        reasons = []
        if isinstance(result, tuple):
            result, reasons = result

        if result is False and self.ctx.negate:
            return True

        if result is True and not self.ctx.negate:
            return True

        return self._make_error(reasons=reasons)