def parse_guards(self, scope):
        """Parse guards on mixin.
        args:
            scope (Scope): current scope
        raises:
            SyntaxError
        returns:
            bool (passes guards)
        """
        if self.guards:
            cor = True if ',' in self.guards else False
            for g in self.guards:
                if isinstance(g, list):
                    res = (g[0].parse(scope)
                           if len(g) == 1 else Expression(g).parse(scope))
                    if cor:
                        if res:
                            return True
                    elif not res:
                        return False
        return True