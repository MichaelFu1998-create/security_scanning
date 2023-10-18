def doesmenuitemexist(self, window_name, object_name):
        """
        Check a menu item exist.

        @param window_name: Window name to look for, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to look for, either full name,
        LDTP's name convention, or a Unix glob. Or menu heirarchy
        @type object_name: string
        @param strict_hierarchy: Mandate menu hierarchy if set to True
        @type object_name: boolean

        @return: 1 on success.
        @rtype: integer
        """
        try:
            menu_handle = self._get_menu_handle(window_name, object_name,
                                                False)
            return 1
        except LdtpServerException:
            return 0