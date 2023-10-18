def verifydropdown(self, window_name, object_name):
        """
        Verify drop down list / menu poped up
        
        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob. 
        @type object_name: string

        @return: 1 on success 0 on failure.
        @rtype: integer
        """
        try:
            object_handle = self._get_object_handle(window_name, object_name)
            if not object_handle.AXEnabled or not object_handle.AXChildren:
                return 0
            # Get AXMenu
            children = object_handle.AXChildren[0]
            if children:
                return 1
        except LdtpServerException:
            pass
        return 0