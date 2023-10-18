def max(self, constraints, X: BitVec, M=10000):
        """
        Iteratively finds the maximum value for a symbol within given constraints.
        :param X: a symbol or expression
        :param M: maximum number of iterations allowed
        """
        assert isinstance(X, BitVec)
        return self.optimize(constraints, X, 'maximize', M)