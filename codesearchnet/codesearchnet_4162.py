def t_text(self, t):
        r':\s*<text>'
        t.lexer.text_start = t.lexer.lexpos - len('<text>')
        t.lexer.begin('text')