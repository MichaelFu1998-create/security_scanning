def verifytabname(self, window_name, object_name, tab_name):
        """
        Verify tab name.
        
        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob. 
        @type object_name: string
        @param tab_name: tab to select
        @type data: string

        @return: 1 on success 0 on failure
        @rtype: integer
        """
        try:
            tab_handle = self._get_tab_handle(window_name, object_name, tab_name)
            if tab_handle.AXValue:
                return 1
        except LdtpServerException:
            pass
        return 0