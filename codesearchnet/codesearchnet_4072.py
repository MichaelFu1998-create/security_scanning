def t_heredoc(self, t):
        r'<<\S+\r?\n'
        t.lexer.is_tabbed = False
        self._init_heredoc(t)
        t.lexer.begin('heredoc')