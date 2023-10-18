def p_block(self, p):
        """ block_decl               : block_open declaration_list brace_close
        """
        p[0] = Block(list(p)[1:-1], p.lineno(3))
        self.scope.pop()
        self.scope.add_block(p[0])