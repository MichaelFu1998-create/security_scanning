def tf_solve(self, fn_x, x_init, b):
        """
        Iteratively solves the system of linear equations $A x = b$.

        Args:
            fn_x: A callable returning the left-hand side $A x$ of the system of linear equations.
            x_init: Initial solution guess $x_0$, zero vector if None.
            b: The right-hand side $b$ of the system of linear equations.

        Returns:
            A solution $x$ to the problem as given by the solver.
        """
        return super(ConjugateGradient, self).tf_solve(fn_x, x_init, b)