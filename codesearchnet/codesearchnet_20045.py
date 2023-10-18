def remove_listener(self, event, listener):
        """Remove a listener from the emitter.

        Args:
            event (str): The event name on which the listener is bound.
            listener: A reference to the same object given to add_listener.

        Returns:
            bool: True if a listener was removed else False.

        This method only removes one listener at a time. If a listener is
        attached multiple times then this method must be called repeatedly.
        Additionally, this method removes listeners first from the those
        registered with 'on' or 'add_listener'. If none are found it continue
        to remove afterwards from those added with 'once'.
        """
        with contextlib.suppress(ValueError):

            self._listeners[event].remove(listener)
            return True

        with contextlib.suppress(ValueError):

            self._once[event].remove(listener)
            return True

        return False