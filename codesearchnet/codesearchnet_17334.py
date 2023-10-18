def getobjectlist(self, window_name):
        """
        Get list of items in given GUI.

        @param window_name: Window name to look for, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string

        @return: list of items in LDTP naming convention.
        @rtype: list
        """
        try:
            window_handle, name, app = self._get_window_handle(window_name, True)
            object_list = self._get_appmap(window_handle, name, True)
        except atomac._a11y.ErrorInvalidUIElement:
            # During the test, when the window closed and reopened
            # ErrorInvalidUIElement exception will be thrown
            self._windows = {}
            # Call the method again, after updating apps
            window_handle, name, app = self._get_window_handle(window_name, True)
            object_list = self._get_appmap(window_handle, name, True)
        return object_list.keys()