def p_block_open(self, p):
        """ block_open                : identifier brace_open
        """
        try:
            p[1].parse(self.scope)
        except SyntaxError:
            pass
        p[0] = p[1]
        self.scope.current = p[1]