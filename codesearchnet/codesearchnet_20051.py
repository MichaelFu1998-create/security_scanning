def count(self, event):
        """Get the number of listeners for the event.

        Args:
            event (str): The event for which to count all listeners.

        The resulting count is a combination of listeners added using
        'on'/'add_listener' and 'once'.
        """
        return len(self._listeners[event]) + len(self._once[event])