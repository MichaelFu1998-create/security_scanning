def selectrowindex(self, window_name, object_name, row_index):
        """
        Select row index

        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob. 
        @type object_name: string
        @param row_index: Row index to select
        @type row_index: integer

        @return: 1 on success.
        @rtype: integer
        """
        object_handle = self._get_object_handle(window_name, object_name)
        if not object_handle.AXEnabled:
            raise LdtpServerException(u"Object %s state disabled" % object_name)

        count = len(object_handle.AXRows)
        if row_index < 0 or row_index > count:
            raise LdtpServerException('Row index out of range: %d' % row_index)
        cell = object_handle.AXRows[row_index]
        if not cell.AXSelected:
            object_handle.activate()
            cell.AXSelected = True
        else:
            # Selected
            pass
        return 1