def _rows(self, spec):
        """Parse a collection of rows."""
        rows = self.new_row_collection()
        for row in spec:
            rows.append(self._row(row))
        return rows