def _apply_record_length_checks(self, i, r, summarize=False, context=None):
        """Apply record length checks on the given record `r`."""

        for code, message, modulus in self._record_length_checks:
            if i % modulus == 0: # support sampling
                if len(r) != len(self._field_names):
                    p = {'code': code}
                    if not summarize:
                        p['message'] = message
                        p['row'] = i + 1
                        p['record'] = r
                        p['length'] = len(r)
                        if context is not None: p['context'] = context
                    yield p