def p_Objects(self, p):
        """Objects : Objects ',' Object
                   | Object"""
        n = len(p)
        if n == 4:
            p[0] = ('Objects', p[1][1] + [p[3]])
        elif n == 2:
            p[0] = ('Objects', [p[1]])