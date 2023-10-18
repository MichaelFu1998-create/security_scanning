def p_Value(self, p):
        """Value : valueofObjectSyntax
                 | '{' BitsValue '}'"""
        n = len(p)
        if n == 2:
            p[0] = p[1]
        elif n == 4:
            p[0] = p[2]