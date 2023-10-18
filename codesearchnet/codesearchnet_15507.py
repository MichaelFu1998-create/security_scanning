def call(self, scope, args=[]):
        """Call mixin. Parses a copy of the mixins body
        in the current scope and returns it.
        args:
            scope (Scope): current scope
            args (list): arguments
        raises:
            SyntaxError
        returns:
            list or False
        """
        ret = False
        if args:
            args = [[
                a.parse(scope) if isinstance(a, Expression) else a for a in arg
            ] if arg else arg for arg in args]
        try:
            self.parse_args(args, scope)
        except SyntaxError:
            pass
        else:
            if self.parse_guards(scope):
                body = self.body.copy()
                ret = body.tokens[1]
                if ret:
                    utility.rename(ret, scope, Block)
        return ret