def _apply_value_checks(self, i, r,
                            summarize=False,
                            report_unexpected_exceptions=True,
                            context=None):
        """Apply value check functions on the given record `r`."""

        for field_name, check, code, message, modulus in self._value_checks:
            if i % modulus == 0: # support sampling
                fi = self._field_names.index(field_name)
                if fi < len(r): # only apply checks if there is a value
                    value = r[fi]
                    try:
                        check(value)
                    except ValueError:
                        p = {'code': code}
                        if not summarize:
                            p['message'] = message
                            p['row'] = i + 1
                            p['column'] = fi + 1
                            p['field'] = field_name
                            p['value'] = value
                            p['record'] = r
                            if context is not None: p['context'] = context
                        yield p
                    except Exception as e:
                        if report_unexpected_exceptions:
                            p = {'code': UNEXPECTED_EXCEPTION}
                            if not summarize:
                                p['message'] = MESSAGES[UNEXPECTED_EXCEPTION] % (e.__class__.__name__, e)
                                p['row'] = i + 1
                                p['column'] = fi + 1
                                p['field'] = field_name
                                p['value'] = value
                                p['record'] = r
                                p['exception'] = e
                                p['function'] = '%s: %s' % (check.__name__,
                                                            check.__doc__)
                                if context is not None: p['context'] = context
                            yield p