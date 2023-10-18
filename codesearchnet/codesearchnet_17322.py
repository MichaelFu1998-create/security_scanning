def getcellvalue(self, window_name, object_name, row_index, column=0):
        """
        Get cell value

        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob. 
        @type object_name: string
        @param row_index: Row index to get
        @type row_index: integer
        @param column: Column index to get, default value 0
        @type column: integer

        @return: cell value on success.
        @rtype: string
        """
        object_handle = self._get_object_handle(window_name, object_name)
        if not object_handle.AXEnabled:
            raise LdtpServerException(u"Object %s state disabled" % object_name)

        count = len(object_handle.AXRows)
        if row_index < 0 or row_index > count:
            raise LdtpServerException('Row index out of range: %d' % row_index)
        cell = object_handle.AXRows[row_index]
        count = len(cell.AXChildren)
        if column < 0 or column > count:
            raise LdtpServerException('Column index out of range: %d' % column)
        obj = cell.AXChildren[column]
        if not re.search("AXColumn", obj.AXRole):
            obj = cell.AXChildren[column]
        return obj.AXValue