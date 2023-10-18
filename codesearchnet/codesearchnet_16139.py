def _apply_unique_checks(self, i, r, unique_sets,
                             summarize=False,
                             context=None):
        """Apply unique checks on `r`."""

        for key, code, message in self._unique_checks:
            value = None
            values = unique_sets[key]
            if isinstance(key, basestring): # assume key is a field name
                fi = self._field_names.index(key)
                if fi >= len(r):
                    continue
                value = r[fi]
            else: # assume key is a list or tuple, i.e., compound key
                value = []
                for f in key:
                    fi = self._field_names.index(f)
                    if fi >= len(r):
                        break
                    value.append(r[fi])
                value = tuple(value) # enable hashing
            if value in values:
                p = {'code': code}
                if not summarize:
                    p['message'] = message
                    p['row'] = i + 1
                    p['record'] = r
                    p['key'] = key
                    p['value'] = value
                    if context is not None: p['context'] = context
                yield p
            values.add(value)