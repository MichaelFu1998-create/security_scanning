def indent(self):
        """
        Performs an indentation
        """
        if not self.tab_always_indent:
            super(PyIndenterMode, self).indent()
        else:
            cursor = self.editor.textCursor()
            assert isinstance(cursor, QtGui.QTextCursor)
            if cursor.hasSelection():
                self.indent_selection(cursor)
            else:
                # simply insert indentation at the cursor position
                tab_len = self.editor.tab_length
                cursor.beginEditBlock()
                if self.editor.use_spaces_instead_of_tabs:
                    cursor.insertText(tab_len * " ")
                else:
                    cursor.insertText('\t')
                cursor.endEditBlock()
                self.editor.setTextCursor(cursor)