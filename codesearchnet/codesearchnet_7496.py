def p_enumItems(self, p):
        """enumItems : enumItems ',' enumItem
                     | enumItem"""
        n = len(p)
        if n == 4:
            p[0] = p[1] + [p[3]]
        elif n == 2:
            p[0] = [p[1]]