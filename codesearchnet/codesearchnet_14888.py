def comment(self):
        """
        Comments/Uncomments the selected lines or the current lines if there
        is no selection.
        """
        cursor = self.editor.textCursor()
        # get the indent at which comment should be inserted and whether to
        # comment or uncomment the selected text
        indent, comment, nb_lines = self.get_operation()
        has_selection = cursor.hasSelection()
        if nb_lines > 1:
            self._move_cursor_to_selection_start(cursor)
            cursor.beginEditBlock()
            for i in range(nb_lines):
                self.comment_line(indent, cursor, comment)
                cursor.movePosition(cursor.NextBlock)
            cursor.endEditBlock()
        else:
            # comment a single line
            cursor.beginEditBlock()
            self.comment_line(indent, cursor, comment)
            if not has_selection:
                # move to the first non-whitespace character of the next line
                cursor.movePosition(cursor.NextBlock)
                text = cursor.block().text()
                indent = len(text) - len(text.lstrip())
                cursor.movePosition(cursor.Right, cursor.MoveAnchor, indent)
                cursor.endEditBlock()
                self.editor.setTextCursor(cursor)
            else:
                cursor.endEditBlock()