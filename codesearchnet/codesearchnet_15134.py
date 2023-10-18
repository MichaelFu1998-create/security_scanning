def _pattern(self, base):
        """Parse a pattern."""
        rows = self._rows(base.get(ROWS, []))
        self._finish_inheritance()
        self._finish_instructions()
        self._connect_rows(base.get(CONNECTIONS, []))
        id_ = self._to_id(base[ID])
        name = base[NAME]
        return self.new_pattern(id_, name, rows)