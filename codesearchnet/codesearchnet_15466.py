def copy(self):
        """ Return a full copy of self
        returns: Block object
        """
        name, inner = self.tokens
        if inner:
            inner = [u.copy() if u else u for u in inner]
        if name:
            name = name.copy()
        return Block([name, inner], 0)