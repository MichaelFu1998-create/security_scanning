def tf_solve(self, fn_x, x_init, base_value, target_value, estimated_improvement=None):
        """
        Iteratively optimizes $f(x)$ for $x$ on the line between $x'$ and $x_0$.

        Args:
            fn_x: A callable returning the value $f(x)$ at $x$.
            x_init: Initial solution guess $x_0$.
            base_value: Value $f(x')$ at $x = x'$.
            target_value: Value $f(x_0)$ at $x = x_0$.
            estimated_improvement: Estimated improvement for $x = x_0$, $f(x')$ if None.

        Returns:
            A solution $x$ to the problem as given by the solver.
        """
        return super(LineSearch, self).tf_solve(fn_x, x_init, base_value, target_value, estimated_improvement)