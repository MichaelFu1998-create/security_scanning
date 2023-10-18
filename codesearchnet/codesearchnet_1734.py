def line(self):
        """
        Returns the line number of the beginning of this range.
        """
        line, column = self.source_buffer.decompose_position(self.begin_pos)
        return line