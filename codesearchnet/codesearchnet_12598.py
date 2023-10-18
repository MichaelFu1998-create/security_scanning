def observe(matcher):
        """
        Internal decorator to trigger operator hooks before/after
        matcher execution.
        """
        @functools.wraps(matcher)
        def observer(self, subject, *expected, **kw):
            # Trigger before hook, if present
            if hasattr(self, 'before'):
                self.before(subject, *expected, **kw)

            # Trigger matcher method
            result = matcher(self, subject, *expected, **kw)

            # After error hook
            if result is not True and hasattr(self, 'after_error'):
                self.after_error(result, subject, *expected, **kw)

            # After success hook
            if result is True and hasattr(self, 'after_success'):
                self.after_success(subject, *expected, **kw)

            # Enable diff comparison on error, if needed
            if not hasattr(self, 'show_diff'):
                self.show_diff = all([
                    isinstance(subject, six.string_types),
                    all([isinstance(x, six.string_types) for x in expected]),
                ])

            return result
        return observer