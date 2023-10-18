def p_IndexTypes(self, p):
        """IndexTypes : IndexTypes ',' IndexType
                      | IndexType"""
        n = len(p)
        if n == 4:
            p[0] = p[1] + [p[3]]
        elif n == 2:
            p[0] = [p[1]]