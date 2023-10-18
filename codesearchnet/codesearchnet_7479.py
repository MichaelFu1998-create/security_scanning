def p_declarations(self, p):
        """declarations : declarations declaration
                        | declaration"""
        n = len(p)
        if n == 3:
            p[0] = p[1] + [p[2]]
        elif n == 2:
            p[0] = [p[1]]