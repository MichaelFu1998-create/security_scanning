def disconnect(self, callback):
        """
        Disconnects the signal from the given function.

        :type  callback: object
        :param callback: The callback function.
        """
        if self.weak_subscribers is not None:
            with self.lock:
                index = self._weakly_connected_index(callback)
                if index is not None:
                    self.weak_subscribers.pop(index)[0]
        if self.hard_subscribers is not None:
            try:
                index = self._hard_callbacks().index(callback)
            except ValueError:
                pass
            else:
                self.hard_subscribers.pop(index)