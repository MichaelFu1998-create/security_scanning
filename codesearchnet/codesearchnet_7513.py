def p_MandatoryGroups(self, p):
        """MandatoryGroups : MandatoryGroups ',' MandatoryGroup
                           | MandatoryGroup"""
        n = len(p)
        if n == 4:
            p[0] = ('MandatoryGroups', p[1][1] + [p[3]])
        elif n == 2:
            p[0] = ('MandatoryGroups', [p[1]])