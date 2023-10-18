def parse(self, scope):
        """Parse node.
        args:
            scope (Scope): Current scope
        raises:
            SyntaxError
        returns:
            self
        """
        self.keyframe, = [
            e[0] if isinstance(e, tuple) else e for e in self.tokens
            if str(e).strip()
        ]
        self.subparse = False
        return self