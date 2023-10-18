def selecttab(self, window_name, object_name, tab_name):
        """
        Select tab based on name.
        
        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob. 
        @type object_name: string
        @param tab_name: tab to select
        @type data: string

        @return: 1 on success.
        @rtype: integer
        """
        tab_handle = self._get_tab_handle(window_name, object_name, tab_name)
        tab_handle.Press()
        return 1