def onwindowcreate(self, window_name, fn_name, *args):
        """
        On window create, call the function with given arguments

        @param window_name: Window name to look for, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param fn_name: Callback function
        @type fn_name: function
        @param *args: arguments to be passed to the callback function
        @type *args: var args

        @return: 1 if registration was successful, 0 if not.
        @rtype: integer
        """
        self._pollEvents._callback[window_name] = ["onwindowcreate", fn_name, args]
        return self._remote_onwindowcreate(window_name)