def source_line(self, lineno):
        """
        Returns line ``lineno`` from source, taking ``first_line`` into account,
        or raises :exc:`IndexError` if ``lineno`` is out of range.
        """
        line_begins = self._extract_line_begins()
        lineno = lineno - self.first_line
        if lineno >= 0 and lineno + 1 < len(line_begins):
            first, last = line_begins[lineno:lineno + 2]
            return self.source[first:last]
        elif lineno >= 0 and lineno < len(line_begins):
            return self.source[line_begins[-1]:]
        else:
            raise IndexError