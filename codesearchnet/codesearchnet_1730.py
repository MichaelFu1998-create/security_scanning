def begin(self):
        """
        Returns a zero-length range located just before the beginning of this range.
        """
        return Range(self.source_buffer, self.begin_pos, self.begin_pos,
                     expanded_from=self.expanded_from)