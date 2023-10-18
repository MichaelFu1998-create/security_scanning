def t_css_string(self, t):
        r'"[^"@]*"|\'[^\'@]*\''
        t.lexer.lineno += t.value.count('\n')
        return t