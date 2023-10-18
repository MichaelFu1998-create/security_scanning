def _apply_skips(self, i, r,
                     summarize=False,
                     report_unexpected_exceptions=True,
                     context=None):
        """Apply skip functions on `r`."""

        for skip in self._skips:
            try:
                result = skip(r)
                if result is True:
                    yield True
            except Exception as e:
                if report_unexpected_exceptions:
                    p = {'code': UNEXPECTED_EXCEPTION}
                    if not summarize:
                        p['message'] = MESSAGES[UNEXPECTED_EXCEPTION] % (e.__class__.__name__, e)
                        p['row'] = i + 1
                        p['record'] = r
                        p['exception'] = e
                        p['function'] = '%s: %s' % (skip.__name__,
                                                    skip.__doc__)
                        if context is not None: p['context'] = context
                    yield p