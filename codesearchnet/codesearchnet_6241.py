def __build_problem(self):
        """Build the matrix representation of the sampling problem."""

        # Set up the mathematical problem
        prob = constraint_matrices(self.model, zero_tol=self.feasibility_tol)

        # check if there any non-zero equality constraints
        equalities = prob.equalities
        b = prob.b
        bounds = np.atleast_2d(prob.bounds).T
        var_bounds = np.atleast_2d(prob.variable_bounds).T
        homogeneous = all(np.abs(b) < self.feasibility_tol)
        fixed_non_zero = np.abs(prob.variable_bounds[:, 1]) > \
            self.feasibility_tol
        fixed_non_zero &= prob.variable_fixed

        # check if there are any non-zero fixed variables, add them as
        # equalities to the stoichiometric matrix
        if any(fixed_non_zero):
            n_fixed = fixed_non_zero.sum()
            rows = np.zeros((n_fixed, prob.equalities.shape[1]))
            rows[range(n_fixed), np.where(fixed_non_zero)] = 1.0
            equalities = np.vstack([equalities, rows])
            var_b = prob.variable_bounds[:, 1]
            b = np.hstack([b, var_b[fixed_non_zero]])
            homogeneous = False

        # Set up a projection that can cast point into the nullspace
        nulls = nullspace(equalities)

        # convert bounds to a matrix and add variable bounds as well
        return Problem(
            equalities=shared_np_array(equalities.shape, equalities),
            b=shared_np_array(b.shape, b),
            inequalities=shared_np_array(prob.inequalities.shape,
                                         prob.inequalities),
            bounds=shared_np_array(bounds.shape, bounds),
            variable_fixed=shared_np_array(prob.variable_fixed.shape,
                                           prob.variable_fixed, integer=True),
            variable_bounds=shared_np_array(var_bounds.shape, var_bounds),
            nullspace=shared_np_array(nulls.shape, nulls),
            homogeneous=homogeneous
        )