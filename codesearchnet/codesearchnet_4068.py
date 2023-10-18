def t_string_escapedchar(self, t):
        # If a quote or backslash is escaped, build up the string by ignoring
        # the escape character. Should this be done for other characters?
        r'(?<=\\)(\"|\\)'
        t.lexer.string_value += (
            t.lexer.lexdata[t.lexer.rel_pos : t.lexer.lexpos - 2] + t.value
        )
        t.lexer.rel_pos = t.lexer.lexpos
        pass