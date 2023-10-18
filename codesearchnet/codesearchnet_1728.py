def decompose_position(self, offset):
        """
        Returns a ``line, column`` tuple for a character offset into the source,
        orraises :exc:`IndexError` if ``lineno`` is out of range.
        """
        line_begins = self._extract_line_begins()
        lineno = bisect.bisect_right(line_begins, offset) - 1
        if offset >= 0 and offset <= len(self.source):
            return lineno + self.first_line, offset - line_begins[lineno]
        else:
            raise IndexError