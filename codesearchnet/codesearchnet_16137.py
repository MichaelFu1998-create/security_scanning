def _apply_record_checks(self, i, r,
                                 summarize=False,
                                 report_unexpected_exceptions=True,
                                 context=None):
        """Apply record checks on `r`."""

        for check, modulus in self._record_checks:
            if i % modulus == 0: # support sampling
                rdict = self._as_dict(r)
                try:
                    check(rdict)
                except RecordError as e:
                    code = e.code if e.code is not None else RECORD_CHECK_FAILED
                    p = {'code': code}
                    if not summarize:
                        message = e.message if e.message is not None else MESSAGES[RECORD_CHECK_FAILED]
                        p['message'] = message
                        p['row'] = i + 1
                        p['record'] = r
                        if context is not None: p['context'] = context
                        if e.details is not None: p['details'] = e.details
                    yield p
                except Exception as e:
                    if report_unexpected_exceptions:
                        p = {'code': UNEXPECTED_EXCEPTION}
                        if not summarize:
                            p['message'] = MESSAGES[UNEXPECTED_EXCEPTION] % (e.__class__.__name__, e)
                            p['row'] = i + 1
                            p['record'] = r
                            p['exception'] = e
                            p['function'] = '%s: %s' % (check.__name__,
                                                        check.__doc__)
                            if context is not None: p['context'] = context
                        yield p