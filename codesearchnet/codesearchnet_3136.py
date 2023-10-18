def _get_offset(self, index):
        """
        Translates the index to the internal offsets.

        self.start   -> 0
        self.start+1 -> 1
        ...
        self.end     -> len(self)
        """
        if not self._in_range(index):
            raise IndexError('Map index out of range')
        if isinstance(index, slice):
            index = slice(index.start - self.start, index.stop - self.start)
        else:
            index -= self.start
        return index