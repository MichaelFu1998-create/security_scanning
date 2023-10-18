def p_subidentifiers(self, p):
        """subidentifiers : subidentifiers subidentifier
                          | subidentifier"""
        n = len(p)
        if n == 3:
            p[0] = p[1] + [p[2]]
        elif n == 2:
            p[0] = [p[1]]