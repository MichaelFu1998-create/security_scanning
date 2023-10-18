def minmax(self, constraints, x, iters=10000):
        """Returns the min and max possible values for x within given constraints"""
        if issymbolic(x):
            m = self.min(constraints, x, iters)
            M = self.max(constraints, x, iters)
            return m, M
        else:
            return x, x