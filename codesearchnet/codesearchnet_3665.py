def constraints(self):
        """
        :rtype tuple
        :return: All constraints represented by this and parent sets.
        """
        if self._parent is not None:
            return tuple(self._constraints) + self._parent.constraints
        return tuple(self._constraints)