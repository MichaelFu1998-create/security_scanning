def column(self):
        """
        Returns a zero-based column number of the beginning of this range.
        """
        line, column = self.source_buffer.decompose_position(self.begin_pos)
        return column