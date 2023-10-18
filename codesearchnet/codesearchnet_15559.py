def p_block_replace(self, p):
        """ block_decl               : identifier t_semicolon
        """
        m = p[1].parse(None)
        block = self.scope.blocks(m.raw())
        if block:
            p[0] = block.copy_inner(self.scope)
        else:
            # fallback to mixin. Allow calls to mixins without parens
            p[0] = Deferred(p[1], None, p.lineno(2))