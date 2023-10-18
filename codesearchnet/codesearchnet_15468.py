def parse(self, scope):
        """Parse node
        args:
            scope (Scope): current scope
        raises:
            SyntaxError
        returns:
            self
        """
        self.parsed = list(utility.flatten(self.tokens))
        if self.parsed[0] == '@import':
            if len(self.parsed) > 4:
                # Media @import
                self.parsed.insert(3, ' ')
        return self