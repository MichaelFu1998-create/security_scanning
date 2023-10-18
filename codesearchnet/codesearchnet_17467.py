def gettabcount(self, window_name, object_name):
        """
        Get tab count.
        
        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob. 
        @type object_name: string

        @return: tab count on success.
        @rtype: integer
        """
        children = self._get_tab_children(window_name, object_name)
        return len(children)