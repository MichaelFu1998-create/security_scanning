def parse(self, data):
        """Parses a license list and returns a License or None if it failed."""
        try:
            return self.yacc.parse(data, lexer=self.lex)
        except:
            return None