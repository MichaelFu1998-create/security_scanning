def _row(self, values):
        """Parse a row."""
        row_id = self._to_id(values[ID])
        row = self._spec.new_row(row_id, values, self)
        if SAME_AS in values:
            self._delay_inheritance(row, self._to_id(values[SAME_AS]))
        self._delay_instructions(row)
        self._id_cache[row_id] = row
        return row