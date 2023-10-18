def t_UPPERCASE_IDENTIFIER(self, t):
        r'[A-Z][-a-zA-z0-9]*'
        if t.value in self.forbidden_words:
            raise error.PySmiLexerError("%s is forbidden" % t.value, lineno=t.lineno)

        if t.value[-1] == '-':
            raise error.PySmiLexerError("Identifier should not end with '-': %s" % t.value, lineno=t.lineno)

        t.type = self.reserved.get(t.value, 'UPPERCASE_IDENTIFIER')

        return t