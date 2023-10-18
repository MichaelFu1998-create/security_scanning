def _handle_indent_between_paren(self, column, line, parent_impl, tc):
        """
        Handle indent between symbols such as parenthesis, braces,...
        """
        pre, post = parent_impl
        next_char = self._get_next_char(tc)
        prev_char = self._get_prev_char(tc)
        prev_open = prev_char in ['[', '(', '{']
        next_close = next_char in [']', ')', '}']
        (open_line, open_symbol_col), (close_line, close_col) = \
            self._get_paren_pos(tc, column)
        open_line_txt = self._helper.line_text(open_line)
        open_line_indent = len(open_line_txt) - len(open_line_txt.lstrip())
        if prev_open:
            post = (open_line_indent + self.editor.tab_length) * ' '
        elif next_close and prev_char != ',':
            post = open_line_indent * ' '
        elif tc.block().blockNumber() == open_line:
            post = open_symbol_col * ' '

        # adapt indent if cursor on closing line and next line have same
        # indent -> PEP8 compliance
        if close_line and close_col:
            txt = self._helper.line_text(close_line)
            bn = tc.block().blockNumber()
            flg = bn == close_line
            next_indent = self._helper.line_indent(bn + 1) * ' '
            if flg and txt.strip().endswith(':') and next_indent == post:
                # | look at how the previous line ( ``':'):`` ) was
                # over-indented, this is actually what we are trying to
                # achieve here
                post += self.editor.tab_length * ' '

        # breaking string
        if next_char in ['"', "'"]:
            tc.movePosition(tc.Left)
        is_string = self._helper.is_comment_or_string(tc, formats=['string'])
        if next_char in ['"', "'"]:
            tc.movePosition(tc.Right)
        if is_string:
            trav = QTextCursor(tc)
            while self._helper.is_comment_or_string(
                    trav, formats=['string']):
                trav.movePosition(trav.Left)
            trav.movePosition(trav.Right)
            symbol = '%s' % self._get_next_char(trav)
            pre += symbol
            post += symbol

        return pre, post