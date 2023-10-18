def join(self, other):
        """
        Returns the smallest possible range spanning both this range and other.
        Raises :exc:`ValueError` if the ranges do not belong to the same
        :class:`Buffer`.
        """
        if self.source_buffer != other.source_buffer:
            raise ValueError
        if self.expanded_from == other.expanded_from:
            expanded_from = self.expanded_from
        else:
            expanded_from = None
        return Range(self.source_buffer,
                     min(self.begin_pos, other.begin_pos),
                     max(self.end_pos, other.end_pos),
                     expanded_from=expanded_from)