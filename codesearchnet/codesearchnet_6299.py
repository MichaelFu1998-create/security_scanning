def slim_optimize(self, error_value=float('nan'), message=None):
        """Optimize model without creating a solution object.

        Creating a full solution object implies fetching shadow prices and
        flux values for all reactions and metabolites from the solver
        object. This necessarily takes some time and in cases where only one
        or two values are of interest, it is recommended to instead use this
        function which does not create a solution object returning only the
        value of the objective. Note however that the `optimize()` function
        uses efficient means to fetch values so if you need fluxes/shadow
        prices for more than say 4 reactions/metabolites, then the total
        speed increase of `slim_optimize` versus `optimize` is  expected to
        be small or even negative depending on how you fetch the values
        after optimization.

        Parameters
        ----------
        error_value : float, None
           The value to return if optimization failed due to e.g.
           infeasibility. If None, raise `OptimizationError` if the
           optimization fails.
        message : string
           Error message to use if the model optimization did not succeed.

        Returns
        -------
        float
            The objective value.
        """
        self.solver.optimize()
        if self.solver.status == optlang.interface.OPTIMAL:
            return self.solver.objective.value
        elif error_value is not None:
            return error_value
        else:
            assert_optimal(self, message)