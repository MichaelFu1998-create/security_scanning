def _apply_header_checks(self, i, r, summarize=False, context=None):
        """Apply header checks on the given record `r`."""

        for code, message in self._header_checks:
            if tuple(r) != self._field_names:
                p = {'code': code}
                if not summarize:
                    p['message'] = message
                    p['row'] = i + 1
                    p['record'] = tuple(r)
                    p['missing'] = set(self._field_names) - set(r)
                    p['unexpected'] = set(r) - set(self._field_names)
                    if context is not None: p['context'] = context
                yield p