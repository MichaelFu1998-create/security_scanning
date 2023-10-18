def t_stringdollar_rbrace(self, t):
        r'\}'
        t.lexer.braces -= 1

        if t.lexer.braces == 0:
            # End of the dollar brace, back to the rest of the string
            t.lexer.begin('string')