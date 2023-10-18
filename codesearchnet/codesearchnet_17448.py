def deregisterevent(self, event_name):
        """
        Remove callback of registered event

        @param event_name: Event name in at-spi format.
        @type event_name: string

        @return: 1 if registration was successful, 0 if not.
        @rtype: integer
        """

        if event_name in self._pollEvents._callback:
            del self._pollEvents._callback[event_name]
        return self._remote_deregisterevent(event_name)