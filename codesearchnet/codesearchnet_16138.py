def _apply_record_predicates(self, i, r,
                                 summarize=False,
                                 report_unexpected_exceptions=True,
                                 context=None):
        """Apply record predicates on `r`."""

        for predicate, code, message, modulus in self._record_predicates:
            if i % modulus == 0: # support sampling
                rdict = self._as_dict(r)
                try:
                    valid = predicate(rdict)
                    if not valid:
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
                            p['function'] = '%s: %s' % (predicate.__name__,
                                                        predicate.__doc__)
                            if context is not None: p['context'] = context
                        yield p