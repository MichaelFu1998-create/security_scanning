def _as_dict(self, r):
        """Convert the record to a dictionary using field names as keys."""

        d = dict()
        for i, f in enumerate(self._field_names):
            d[f] = r[i] if i < len(r) else None
        return d