def _in_range(self, index):
        """ Returns True if index is in range """
        if isinstance(index, slice):
            in_range = index.start < index.stop and \
                index.start >= self.start and \
                index.stop <= self.end
        else:
            in_range = index >= self.start and \
                index <= self.end
        return in_range