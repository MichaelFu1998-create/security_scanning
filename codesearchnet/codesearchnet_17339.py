def activatewindow(self, window_name):
        """
        Activate window.

        @param window_name: Window name to look for, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string

        @return: 1 on success.
        @rtype: integer
        """
        window_handle = self._get_window_handle(window_name)
        self._grabfocus(window_handle)
        return 1