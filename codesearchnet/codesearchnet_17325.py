def doubleclickrowindex(self, window_name, object_name, row_index, col_index=0):
        """
        Double click row matching given text

        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type object_name: string
        @param row_index: Row index to click
        @type row_index: integer
        @param col_index: Column index to click
        @type col_index: integer

        @return: row index matching the text on success.
        @rtype: integer
        """
        object_handle = self._get_object_handle(window_name, object_name)
        if not object_handle.AXEnabled:
            raise LdtpServerException(u"Object %s state disabled" % object_name)

        count = len(object_handle.AXRows)
        if row_index < 0 or row_index > count:
            raise LdtpServerException('Row index out of range: %d' % row_index)
        cell = object_handle.AXRows[row_index]
        self._grabfocus(cell)
        x, y, width, height = self._getobjectsize(cell)
        # Mouse double click on the object
        cell.doubleClickMouse((x + width / 2, y + height / 2))
        return 1