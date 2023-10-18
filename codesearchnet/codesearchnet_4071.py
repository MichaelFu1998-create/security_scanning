def t_tabbedheredoc(self, t):
        r'<<-\S+\r?\n'
        t.lexer.is_tabbed = True
        self._init_heredoc(t)
        t.lexer.begin('tabbedheredoc')