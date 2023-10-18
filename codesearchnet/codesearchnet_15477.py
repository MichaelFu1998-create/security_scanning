def t_t_isopen(self, t):
        r'"|\''
        if t.value[0] == '"':
            t.lexer.push_state('istringquotes')
        elif t.value[0] == '\'':
            t.lexer.push_state('istringapostrophe')
        return t