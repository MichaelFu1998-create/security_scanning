def p_range(self, p):
        """range : value DOT_DOT value
                 | value"""
        n = len(p)
        if n == 2:
            p[0] = (p[1],)
        elif n == 4:
            p[0] = (p[1], p[3])