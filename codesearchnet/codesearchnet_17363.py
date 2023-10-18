def verifymenucheck(self, window_name, object_name):
        """
        Verify a menu item is checked

        @param window_name: Window name to look for, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to look for, either full name,
        LDTP's name convention, or a Unix glob. Or menu heirarchy
        @type object_name: string

        @return: 1 on success.
        @rtype: integer
        """
        try:
            menu_handle = self._get_menu_handle(window_name, object_name,
                                                False)
            try:
                if menu_handle.AXMenuItemMarkChar:
                    # Checked
                    return 1
            except atomac._a11y.Error:
                pass
        except LdtpServerException:
            pass
        return 0