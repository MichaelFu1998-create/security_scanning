def parse(self, scope):
        """Parse node
        args:
            scope (Scope): current scope
        raises:
            SyntaxError
        returns:
            self
        """
        self.name, args, self.guards = self.tokens[0]
        self.args = [a for a in utility.flatten(args) if a]
        self.body = Block([None, self.tokens[1]], 0)
        self.vars = list(
            utility.flatten([
                list(v.values()) for v in [s['__variables__'] for s in scope]
            ]))
        return self