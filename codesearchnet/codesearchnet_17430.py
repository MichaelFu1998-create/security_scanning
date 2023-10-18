def inserttext(self, window_name, object_name, position, data):
        """
        Insert string sequence in given position.
        
        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob. 
        @type object_name: string
        @param position: position where text has to be entered.
        @type data: int
        @param data: data to type.
        @type data: string

        @return: 1 on success.
        @rtype: integer
        """
        object_handle = self._get_object_handle(window_name, object_name)
        if not object_handle.AXEnabled:
            raise LdtpServerException(u"Object %s state disabled" % object_name)
        existing_data = object_handle.AXValue
        size = len(existing_data)
        if position < 0:
            position = 0
        if position > size:
            position = size
        object_handle.AXValue = existing_data[:position] + data + \
                                existing_data[position:]
        return 1