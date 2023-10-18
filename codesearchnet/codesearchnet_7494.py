def p_ranges(self, p):
        """ranges : ranges '|' range
                  | range"""
        n = len(p)
        if n == 4:
            p[0] = p[1] + [p[3]]
        elif n == 2:
            p[0] = [p[1]]