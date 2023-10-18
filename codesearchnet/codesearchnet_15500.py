def parse(self, scope):
        """Parse node
        args:
            scope (Scope): current scope
        raises:
            SyntaxError
        returns:
            self
        """
        if not self.parsed:
            if len(self.tokens) > 2:
                property, style, _ = self.tokens
                self.important = True
            else:
                property, style = self.tokens
                self.important = False
            self.property = ''.join(property)
            self.parsed = []
            if style:
                style = self.preprocess(style)
                self.parsed = self.process(style, scope)
        return self