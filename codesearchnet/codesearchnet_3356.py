def min(self, constraints, X: BitVec, M=10000):
        """
        Iteratively finds the minimum value for a symbol within given constraints.

        :param constraints: constraints that the expression must fulfil
        :param X: a symbol or expression
        :param M: maximum number of iterations allowed
        """
        assert isinstance(X, BitVec)
        return self.optimize(constraints, X, 'minimize', M)