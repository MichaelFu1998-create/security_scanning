def pastetext(self, window_name, object_name, position=0):
        """
        paste text from start position to end position
        
        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob. 
        @type object_name: string
        @param position: Position to paste the text, default 0
        @type object_name: integer

        @return: 1 on success.
        @rtype: integer
        """
        object_handle = self._get_object_handle(window_name, object_name)
        if not object_handle.AXEnabled:
            raise LdtpServerException(u"Object %s state disabled" % object_name)
        size = object_handle.AXNumberOfCharacters
        if position > size:
            position = size
        if position < 0:
            position = 0
        clipboard = Clipboard.paste()
        data = object_handle.AXValue
        object_handle.AXValue = data[:position] + clipboard + data[position:]
        return 1