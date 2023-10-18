def add_observer(self, callback):
        """Add an observer to this event.

        Args:
            callback: A function or coroutine callback to call when the event
                is fired.

        Raises:
            ValueError: If the callback has already been added.
        """
        if callback in self._observers:
            raise ValueError('{} is already an observer of {}'
                             .format(callback, self))
        self._observers.append(callback)