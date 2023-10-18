def grabfocus(self, window_name, object_name=None):
        """
        Grab focus.

        @param window_name: Window name to look for, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to look for, either full name,
        LDTP's name convention, or a Unix glob.
        @type object_name: string

        @return: 1 on success.
        @rtype: integer
        """
        if not object_name:
            handle, name, app = self._get_window_handle(window_name)
        else:
            handle = self._get_object_handle(window_name, object_name)
        return self._grabfocus(handle)