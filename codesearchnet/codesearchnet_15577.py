def parse(self, scope):
        """Parse node
        args:
            scope (Scope): current scope
        raises:
            SyntaxError
        returns:
            parsed
        """
        if not self.parsed:
            self.parsed = ''.join(self.process(self.tokens, scope))
        return self.parsed