def rewrite(self):
        """Return the rewritten source. May raise :class:`RewriterConflict`."""
        self._sort()
        self._check()

        rewritten, pos = [], 0
        for range, replacement in self.ranges:
            rewritten.append(self.buffer.source[pos:range.begin_pos])
            rewritten.append(replacement)
            pos = range.end_pos
        rewritten.append(self.buffer.source[pos:])

        return Buffer("".join(rewritten), self.buffer.name, self.buffer.first_line)