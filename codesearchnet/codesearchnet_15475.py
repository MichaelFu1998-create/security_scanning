def t_t_eopen(self, t):
        r'~"|~\''
        if t.value[1] == '"':
            t.lexer.push_state('escapequotes')
        elif t.value[1] == '\'':
            t.lexer.push_state('escapeapostrophe')
        return t