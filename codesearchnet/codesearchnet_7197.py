def remove_observer(self, callback):
        """Remove an observer from this event.

        Args:
            callback: A function or coroutine callback to remove from this
                event.

        Raises:
            ValueError: If the callback is not an observer of this event.
        """
        if callback not in self._observers:
            raise ValueError('{} is not an observer of {}'
                             .format(callback, self))
        self._observers.remove(callback)