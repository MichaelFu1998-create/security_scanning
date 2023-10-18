def p_BitNames(self, p):
        """BitNames : BitNames ',' LOWERCASE_IDENTIFIER
                    | LOWERCASE_IDENTIFIER"""
        n = len(p)
        if n == 4:
            p[0] = ('BitNames', p[1][1] + [p[3]])
        elif n == 2:
            p[0] = ('BitNames', [p[1]])