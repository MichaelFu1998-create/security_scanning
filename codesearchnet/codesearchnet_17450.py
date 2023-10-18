def deregisterkbevent(self, keys, modifiers):
        """
        Remove callback of registered event

        @param keys: key to listen
        @type keys: string
        @param modifiers: control / alt combination using gtk MODIFIERS
        @type modifiers: int

        @return: 1 if registration was successful, 0 if not.
        @rtype: integer
        """

        event_name = "kbevent%s%s" % (keys, modifiers)
        if event_name in _pollEvents._callback:
            del _pollEvents._callback[event_name]
        return self._remote_deregisterkbevent(keys, modifiers)