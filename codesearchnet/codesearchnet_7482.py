def p_Syntax(self, p):
        """Syntax : ObjectSyntax
                  | BITS '{' NamedBits '}'"""
        # libsmi: TODO: standalone `BITS' ok? seen in RMON2-MIB
        # libsmi: -> no, it's only allowed in a SEQUENCE {...}
        n = len(p)
        if n == 2:
            p[0] = p[1]
        elif n == 5:
            p[0] = (p[1], p[3])