def is_connected(self, callback):
        """
        Returns True if the event is connected to the given function.

        :type  callback: object
        :param callback: The callback function.
        :rtype:  bool
        :returns: Whether the signal is connected to the given function.
        """
        index = self._weakly_connected_index(callback)
        if index is not None:
            return True
        if self.hard_subscribers is None:
            return False
        return callback in self._hard_callbacks()