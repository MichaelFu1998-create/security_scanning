def chain(self, expanded_from):
        """
        Returns a range identical to this one, but indicating that
        it was expanded from the range `expanded_from`.
        """
        return Range(self.source_buffer, self.begin_pos, self.begin_pos,
                     expanded_from=expanded_from)