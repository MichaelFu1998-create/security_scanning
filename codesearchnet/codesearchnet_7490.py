def p_valueofSimpleSyntax(self, p):
        """valueofSimpleSyntax : NUMBER
                               | NEGATIVENUMBER
                               | NUMBER64
                               | NEGATIVENUMBER64
                               | HEX_STRING
                               | BIN_STRING
                               | LOWERCASE_IDENTIFIER
                               | QUOTED_STRING
                               | '{' objectIdentifier_defval '}'"""
        # libsmi for objectIdentifier_defval:
        # This is only for some MIBs with invalid numerical
        # OID notation for DEFVALs. We DO NOT parse them
        # correctly. We just don't want to produce a
        # parser error.
        n = len(p)
        if n == 2:
            p[0] = p[1]
        elif n == 4:  # XXX
            pass