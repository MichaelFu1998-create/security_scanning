def verifyscrollbarvertical(self, window_name, object_name):
        """
        Verify scrollbar is vertical

        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type object_name: string

        @return: 1 on success.
        @rtype: integer
        """
        try:
            object_handle = self._get_object_handle(window_name, object_name)
            if object_handle.AXOrientation == "AXVerticalOrientation":
                return 1
        except:
            pass
        return 0