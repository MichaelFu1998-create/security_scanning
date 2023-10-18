def source_lines(self):
        """
        Returns the lines of source code containing the entirety of this range.
        """
        return [self.source_buffer.source_line(line)
                for line in range(self.line(), self.end().line() + 1)]