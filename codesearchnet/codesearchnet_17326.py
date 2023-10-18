def verifytablecell(self, window_name, object_name, row_index,
                        column_index, row_text):
        """
        Verify table cell value with given text

        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob. 
        @type object_name: string
        @param row_index: Row index to get
        @type row_index: integer
        @param column_index: Column index to get, default value 0
        @type column_index: integer
        @param row_text: Row text to match
        @type string

        @return: 1 on success 0 on failure.
        @rtype: integer
        """
        try:
            value = getcellvalue(window_name, object_name, row_index, column_index)
            if re.match(row_text, value):
                return 1
        except LdtpServerException:
            pass
        return 0