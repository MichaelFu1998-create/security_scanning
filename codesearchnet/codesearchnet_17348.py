def objectexist(self, window_name, object_name):
        """
        Checks whether a window or component exists.

        @param window_name: Window name to look for, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to look for, either full name,
        LDTP's name convention, or a Unix glob.
        @type object_name: string

        @return: 1 if GUI was found, 0 if not.
        @rtype: integer
        """
        try:
            object_handle = self._get_object_handle(window_name, object_name)
            return 1
        except LdtpServerException:
            return 0