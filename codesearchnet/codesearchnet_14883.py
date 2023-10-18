def unindent(self):
        """
        Performs an un-indentation
        """
        if self.tab_always_indent:
            cursor = self.editor.textCursor()
            if not cursor.hasSelection():
                cursor.select(cursor.LineUnderCursor)
            self.unindent_selection(cursor)
        else:
            super(PyIndenterMode, self).unindent()