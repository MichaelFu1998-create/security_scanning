def p_subidentifiers_defval(self, p):
        """subidentifiers_defval : subidentifiers_defval subidentifier_defval
                                 | subidentifier_defval"""
        n = len(p)
        if n == 3:
            p[0] = ('subidentifiers_defval', p[1][1] + [p[2]])
        elif n == 2:
            p[0] = ('subidentifiers_defval', [p[1]])