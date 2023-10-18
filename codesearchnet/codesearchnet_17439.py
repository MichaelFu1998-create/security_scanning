def deletetext(self, window_name, object_name, start_position, end_position=-1):
        """
        delete text from start position to end position
        
        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob. 
        @type object_name: string
        @param start_position: Start position
        @type object_name: integer
        @param end_position: End position, default -1
        Delete all the text from start position till end
        @type object_name: integer

        @return: 1 on success.
        @rtype: integer
        """
        object_handle = self._get_object_handle(window_name, object_name)
        if not object_handle.AXEnabled:
            raise LdtpServerException(u"Object %s state disabled" % object_name)
        size = object_handle.AXNumberOfCharacters
        if end_position == -1 or end_position > size:
            end_position = size
        if start_position < 0:
            start_position = 0
        data = object_handle.AXValue
        object_handle.AXValue = data[:start_position] + data[end_position:]
        return 1