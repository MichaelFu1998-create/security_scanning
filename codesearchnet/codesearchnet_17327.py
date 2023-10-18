def doesrowexist(self, window_name, object_name, row_text,
                     partial_match=False):
        """
        Verify table cell value with given text

        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob. 
        @type object_name: string
        @param row_text: Row text to match
        @type string
        @param partial_match: Find partial match strings
        @type boolean

        @return: 1 on success 0 on failure.
        @rtype: integer
        """
        try:
            object_handle = self._get_object_handle(window_name, object_name)
            if not object_handle.AXEnabled:
                return 0

            for cell in object_handle.AXRows:
                if not partial_match and re.match(row_text,
                                                  cell.AXChildren[0].AXValue):
                    return 1
                elif partial_match and re.search(row_text,
                                                 cell.AXChildren[0].AXValue):
                    return 1
        except LdtpServerException:
            pass
        return 0