def menucheck(self, window_name, object_name):
        """
        Check (click) a menu item.

        @param window_name: Window name to look for, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to look for, either full name,
        LDTP's name convention, or a Unix glob. Or menu heirarchy
        @type object_name: string

        @return: 1 on success.
        @rtype: integer
        """
        menu_handle = self._get_menu_handle(window_name, object_name)
        if not menu_handle.AXEnabled:
            raise LdtpServerException(u"Object %s state disabled" % object_name)
        try:
            if menu_handle.AXMenuItemMarkChar:
                # Already checked
                return 1
        except atomac._a11y.Error:
            pass
        menu_handle.Press()
        return 1