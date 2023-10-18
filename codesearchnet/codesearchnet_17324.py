def doubleclickrow(self, window_name, object_name, row_text):
        """
        Double click row matching given text

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

        object_handle.activate()
        self.wait(1)
        for cell in object_handle.AXRows:
            cell = self._getfirstmatchingchild(cell, "(AXTextField|AXStaticText)")
            if not cell:
                continue
            if re.match(row_text, cell.AXValue):
                x, y, width, height = self._getobjectsize(cell)
                # Mouse double click on the object
                cell.doubleClickMouse((x + width / 2, y + height / 2))
                return 1
        raise LdtpServerException('Unable to get row text: %s' % row_text)