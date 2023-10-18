def end(self):
        """
        Returns a zero-length range located just after the end of this range.
        """
        return Range(self.source_buffer, self.end_pos, self.end_pos,
                     expanded_from=self.expanded_from)