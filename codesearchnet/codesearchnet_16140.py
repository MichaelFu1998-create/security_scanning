def _apply_each_methods(self, i, r,
                            summarize=False,
                            report_unexpected_exceptions=True,
                            context=None):
        """Invoke 'each' methods on `r`."""

        for a in dir(self):
            if a.startswith('each'):
                rdict = self._as_dict(r)
                f = getattr(self, a)
                try:
                    f(rdict)
                except Exception as e:
                    if report_unexpected_exceptions:
                        p = {'code': UNEXPECTED_EXCEPTION}
                        if not summarize:
                            p['message'] = MESSAGES[UNEXPECTED_EXCEPTION] % (e.__class__.__name__, e)
                            p['row'] = i + 1
                            p['record'] = r
                            p['exception'] = e
                            p['function'] = '%s: %s' % (f.__name__,
                                                        f.__doc__)
                            if context is not None: p['context'] = context
                        yield p