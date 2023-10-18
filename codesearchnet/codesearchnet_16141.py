def _apply_assert_methods(self, i, r,
                              summarize=False,
                              report_unexpected_exceptions=True,
                              context=None):
        """Apply 'assert' methods on `r`."""

        for a in dir(self):
            if a.startswith('assert'):
                rdict = self._as_dict(r)
                f = getattr(self, a)
                try:
                    f(rdict)
                except AssertionError as e:
                    code = ASSERT_CHECK_FAILED
                    message = MESSAGES[ASSERT_CHECK_FAILED]
                    if len(e.args) > 0:
                        custom = e.args[0]
                        if isinstance(custom, (list, tuple)):
                            if len(custom) > 0:
                                code = custom[0]
                            if len(custom) > 1:
                                message = custom[1]
                        else:
                            code = custom
                    p = {'code': code}
                    if not summarize:
                        p['message'] = message
                        p['row'] = i + 1
                        p['record'] = r
                        if context is not None: p['context'] = context
                    yield p
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