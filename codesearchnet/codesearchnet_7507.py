def p_subidentifier_defval(self, p):
        """subidentifier_defval : LOWERCASE_IDENTIFIER '(' NUMBER ')'
                                | NUMBER"""
        n = len(p)
        if n == 2:
            p[0] = ('subidentifier_defval', p[1])
        elif n == 5:
            p[0] = ('subidentifier_defval', p[1], p[3])