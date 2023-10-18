def multiselect(self, window_name, object_name, row_text_list, partial_match=False):
        """
        Select multiple row

        @param window_name: Window name to type in, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param object_name: Object name to type in, either full name,
        LDTP's name convention, or a Unix glob. 
        @type object_name: string
        @param row_text_list: Row list with matching text to select
        @type row_text: string

        @return: 1 on success.
        @rtype: integer
        """
        object_handle = self._get_object_handle(window_name, object_name)
        if not object_handle.AXEnabled:
            raise LdtpServerException(u"Object %s state disabled" % object_name)

        object_handle.activate()
        selected = False
        try:
            window = self._get_front_most_window()
        except (IndexError,):
            window = self._get_any_window()
        for row_text in row_text_list:
            selected = False
            for cell in object_handle.AXRows:
                parent_cell = cell
                cell = self._getfirstmatchingchild(cell, "(AXTextField|AXStaticText)")
                if not cell:
                    continue
                if re.match(row_text, cell.AXValue):
                    selected = True
                    if not parent_cell.AXSelected:
                        x, y, width, height = self._getobjectsize(parent_cell)
                        window.clickMouseButtonLeftWithMods((x + width / 2,
                                                             y + height / 2),
                                                            ['<command_l>'])
                        # Following selection doesn't work
                        # parent_cell.AXSelected=True
                        self.wait(0.5)
                    else:
                        # Selected
                        pass
                    break
            if not selected:
                raise LdtpServerException(u"Unable to select row: %s" % row_text)
        if not selected:
            raise LdtpServerException(u"Unable to select any row")
        return 1