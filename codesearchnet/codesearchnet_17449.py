def registerkbevent(self, keys, modifiers, fn_name, *args):
        """
        Register keystroke events

        @param keys: key to listen
        @type keys: string
        @param modifiers: control / alt combination using gtk MODIFIERS
        @type modifiers: int
        @param fn_name: Callback function
        @type fn_name: function
        @param *args: arguments to be passed to the callback function
        @type *args: var args

        @return: 1 if registration was successful, 0 if not.
        @rtype: integer
        """
        event_name = "kbevent%s%s" % (keys, modifiers)
        self._pollEvents._callback[event_name] = [event_name, fn_name, args]
        return self._remote_registerkbevent(keys, modifiers)