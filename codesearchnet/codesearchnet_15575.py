def p_error(self, t):
        """ Internal error handler
        args:
            t (Lex token): Error token
        """
        if t:
            error_msg = "E: %s line: %d, Syntax Error, token: `%s`, `%s`" % \
                      (self.target, t.lineno, t.type, t.value)
            self.register.register(error_msg)
        while True:
            t = self.lex.token()
            if not t or t.value == '}':
                if len(self.scope) > 1:
                    self.scope.pop()
                break
        self.parser.restart()
        return t