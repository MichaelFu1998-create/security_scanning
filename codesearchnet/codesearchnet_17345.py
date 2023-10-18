def guiexist(self, window_name, object_name=None):
        """
        Checks whether a window or component exists.

        @param window_name: Window name to look for, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to look for, either full name,
        LDTP's name convention, or a Unix glob.
        @type object_name: string

        @return: 1 on success.
        @rtype: integer
        """
        try:
            self._windows = {}
            if not object_name:
                handle, name, app = self._get_window_handle(window_name, False)
            else:
                handle = self._get_object_handle(window_name, object_name,
                                                 wait_for_object=False,
                                                 force_remap=True)
            # If window and/or object exist, exception will not be thrown
            # blindly return 1
            return 1
        except LdtpServerException:
            pass
        return 0