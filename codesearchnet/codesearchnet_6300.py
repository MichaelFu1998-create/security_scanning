def optimize(self, objective_sense=None, raise_error=False):
        """
        Optimize the model using flux balance analysis.

        Parameters
        ----------
        objective_sense : {None, 'maximize' 'minimize'}, optional
            Whether fluxes should be maximized or minimized. In case of None,
            the previous direction is used.
        raise_error : bool
            If true, raise an OptimizationError if solver status is not
             optimal.

        Notes
        -----
        Only the most commonly used parameters are presented here.  Additional
        parameters for cobra.solvers may be available and specified with the
        appropriate keyword argument.

        """
        original_direction = self.objective.direction
        self.objective.direction = \
            {"maximize": "max", "minimize": "min"}.get(
                objective_sense, original_direction)
        self.slim_optimize()
        solution = get_solution(self, raise_error=raise_error)
        self.objective.direction = original_direction
        return solution