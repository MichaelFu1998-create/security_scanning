def t_text_end(self, t):
        r'</text>\s*'
        t.type = 'TEXT'
        t.value = t.lexer.lexdata[
            t.lexer.text_start:t.lexer.lexpos]
        t.lexer.lineno += t.value.count('\n')
        t.value = t.value.strip()
        t.lexer.begin('INITIAL')
        return t