def p_modules(self, p):
        """modules : modules module
                   | module"""
        n = len(p)
        if n == 3:
            p[0] = p[1] + [p[2]]
        elif n == 2:
            p[0] = [p[1]]