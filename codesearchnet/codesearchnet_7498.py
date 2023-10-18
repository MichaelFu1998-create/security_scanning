def p_IndexType(self, p):
        """IndexType : IMPLIED Index
                     | Index"""
        n = len(p)
        if n == 2:
            p[0] = (0, p[1])
        elif n == 3:
            p[0] = (1, p[2])