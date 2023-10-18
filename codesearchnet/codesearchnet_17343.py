def getobjectsize(self, window_name, object_name=None):
        """
        Get object size

        @param window_name: Window name to look for, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to look for, either full name,
        LDTP's name convention, or a Unix glob. Or menu heirarchy
        @type object_name: string

        @return: x, y, width, height on success.
        @rtype: list
        """
        if not object_name:
            handle, name, app = self._get_window_handle(window_name)
        else:
            handle = self._get_object_handle(window_name, object_name)
        return self._getobjectsize(handle)