def gettextvalue(self, window_name, object_name, startPosition=0, endPosition=0):
        """
        Get text value
        
        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob. 
        @type object_name: string
        @param startPosition: Starting position of text to fetch
        @type: startPosition: int
        @param endPosition: Ending position of text to fetch
        @type: endPosition: int

        @return: text on success.
        @rtype: string
        """
        object_handle = self._get_object_handle(window_name, object_name)
        if not object_handle.AXEnabled:
            raise LdtpServerException(u"Object %s state disabled" % object_name)
        return object_handle.AXValue