def t_LOWERCASE_IDENTIFIER(self, t):
        r'[0-9]*[a-z][-a-zA-z0-9]*'
        if t.value[-1] == '-':
            raise error.PySmiLexerError("Identifier should not end with '-': %s" % t.value, lineno=t.lineno)
        return t