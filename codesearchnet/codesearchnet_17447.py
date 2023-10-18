def registerevent(self, event_name, fn_name, *args):
        """
        Register at-spi event

        @param event_name: Event name in at-spi format.
        @type event_name: string
        @param fn_name: Callback function
        @type fn_name: function
        @param *args: arguments to be passed to the callback function
        @type *args: var args

        @return: 1 if registration was successful, 0 if not.
        @rtype: integer
        """
        if not isinstance(event_name, str):
            raise ValueError("event_name should be string")
        self._pollEvents._callback[event_name] = [event_name, fn_name, args]
        return self._remote_registerevent(event_name)