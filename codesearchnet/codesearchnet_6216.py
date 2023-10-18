def shadow_price(self):
        """
        The shadow price in the most recent solution.

        Shadow price is the dual value of the corresponding constraint in the
        model.

        Warnings
        --------
        * Accessing shadow prices through a `Solution` object is the safer,
          preferred, and only guaranteed to be correct way. You can see how to
          do so easily in the examples.
        * Shadow price is retrieved from the currently defined
          `self._model.solver`. The solver status is checked but there are no
          guarantees that the current solver state is the one you are looking
          for.
        * If you modify the underlying model after an optimization, you will
          retrieve the old optimization values.

        Raises
        ------
        RuntimeError
            If the underlying model was never optimized beforehand or the
            metabolite is not part of a model.
        OptimizationError
            If the solver status is anything other than 'optimal'.

        Examples
        --------
        >>> import cobra
        >>> import cobra.test
        >>> model = cobra.test.create_test_model("textbook")
        >>> solution = model.optimize()
        >>> model.metabolites.glc__D_e.shadow_price
        -0.09166474637510488
        >>> solution.shadow_prices.glc__D_e
        -0.091664746375104883
        """
        try:
            check_solver_status(self._model.solver.status)
            return self._model.constraints[self.id].dual
        except AttributeError:
            raise RuntimeError(
                "metabolite '{}' is not part of a model".format(self.id))
        # Due to below all-catch, which sucks, need to reraise these.
        except (RuntimeError, OptimizationError) as err:
            raise_with_traceback(err)
        # Would love to catch CplexSolverError and GurobiError here.
        except Exception as err:
            raise_from(OptimizationError(
                "Likely no solution exists. Original solver message: {}."
                "".format(str(err))), err)