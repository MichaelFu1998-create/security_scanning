def p_enumItems(self, p):
        """enumItems : enumItems ',' enumItem
                     | enumItem
                     | enumItems enumItem
                     | enumItems ','"""
        n = len(p)
        if n == 4:
            p[0] = p[1] + [p[3]]
        elif n == 2:
            p[0] = [p[1]]
        elif n == 3:  # typo case
            if p[2] == ',':
                p[0] = p[1]
            else:
                p[0] = p[1] + [p[2]]