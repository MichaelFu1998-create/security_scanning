def t_string_STRING(self, t):
        # End of the string
        r'\"'
        t.value = (
            t.lexer.string_value + t.lexer.lexdata[t.lexer.rel_pos : t.lexer.lexpos - 1]
        )
        t.lexer.lineno += t.lexer.lexdata[t.lexer.abs_start : t.lexer.lexpos - 1].count(
            '\n'
        )
        t.lexer.begin('INITIAL')
        return t