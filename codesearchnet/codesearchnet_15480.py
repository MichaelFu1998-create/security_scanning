def file(self, filename):
        """
        Lex file.
        """
        with open(filename) as f:
            self.lexer.input(f.read())
        return self