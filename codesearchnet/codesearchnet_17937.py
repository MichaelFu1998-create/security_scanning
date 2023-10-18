def _p2i(self, param):
        """
        Parameter to indices, returns (coord, index), e.g. for a pos
        pos     : ('x', 100)
        """
        g = param.split('-')
        if len(g) == 3:
            return g[2], int(g[1])
        else:
            raise ValueError('`param` passed as incorrect format')