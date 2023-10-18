def gettabname(self, window_name, object_name, tab_index):
        """
        Get tab name
        
        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob. 
        @type object_name: string
        @param tab_index: Index of tab (zero based index)
        @type object_name: int

        @return: text on success.
        @rtype: string
        """
        children = self._get_tab_children(window_name, object_name)
        length = len(children)
        if tab_index < 0 or tab_index > length:
            raise LdtpServerException(u"Invalid tab index %s" % tab_index)
        tab_handle = children[tab_index]
        if not tab_handle.AXEnabled:
            raise LdtpServerException(u"Object %s state disabled" % object_name)
        return tab_handle.AXTitle