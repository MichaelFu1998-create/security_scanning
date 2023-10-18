def p_EnterprisePart(self, p):
        """EnterprisePart : ENTERPRISE objectIdentifier
                          | ENTERPRISE '{' objectIdentifier '}'"""
        n = len(p)
        if n == 3:
            p[0] = p[2]
        elif n == 5:  # common mistake case
            p[0] = p[3]