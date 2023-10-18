def gettablerowindex(self, window_name, object_name, row_text):
        """
        Get table row index matching given text

        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob. 
        @type object_name: string
        @param row_text: Row text to select
        @type row_text: string

        @return: row index matching the text on success.
        @rtype: integer
        """
        object_handle = self._get_object_handle(window_name, object_name)
        if not object_handle.AXEnabled:
            raise LdtpServerException(u"Object %s state disabled" % object_name)

        index = 0
        for cell in object_handle.AXRows:
            if re.match(row_text,
                        cell.AXChildren[0].AXValue):
                return index
            index += 1
        raise LdtpServerException(u"Unable to find row: %s" % row_text)