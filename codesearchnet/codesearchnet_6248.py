def validate(self, samples):
        """Validate a set of samples for equality and inequality feasibility.

        Can be used to check whether the generated samples and warmup points
        are feasible.

        Parameters
        ----------
        samples : numpy.matrix
            Must be of dimension (n_samples x n_reactions). Contains the
            samples to be validated. Samples must be from fluxes.

        Returns
        -------
        numpy.array
            A one-dimensional numpy array of length containing
            a code of 1 to 3 letters denoting the validation result:

            - 'v' means feasible in bounds and equality constraints
            - 'l' means a lower bound violation
            - 'u' means a lower bound validation
            - 'e' means and equality constraint violation

        """

        samples = np.atleast_2d(samples)
        prob = self.problem

        if samples.shape[1] == len(self.model.reactions):
            S = create_stoichiometric_matrix(self.model)
            b = np.array([self.model.constraints[m.id].lb for m in
                          self.model.metabolites])
            bounds = np.array([r.bounds for r in self.model.reactions]).T
        elif samples.shape[1] == len(self.model.variables):
            S = prob.equalities
            b = prob.b
            bounds = prob.variable_bounds
        else:
            raise ValueError("Wrong number of columns. samples must have a "
                             "column for each flux or variable defined in the "
                             "model!")

        feasibility = np.abs(S.dot(samples.T).T - b).max(axis=1)
        lb_error = (samples - bounds[0, ]).min(axis=1)
        ub_error = (bounds[1, ] - samples).min(axis=1)

        if (samples.shape[1] == len(self.model.variables) and
                prob.inequalities.shape[0]):
            consts = prob.inequalities.dot(samples.T)
            lb_error = np.minimum(
                lb_error,
                (consts - prob.bounds[0, ]).min(axis=1))
            ub_error = np.minimum(
                ub_error,
                (prob.bounds[1, ] - consts).min(axis=1)
            )

        valid = (
            (feasibility < self.feasibility_tol) &
            (lb_error > -self.bounds_tol) &
            (ub_error > -self.bounds_tol))
        codes = np.repeat("", valid.shape[0]).astype(np.dtype((str, 3)))
        codes[valid] = "v"
        codes[lb_error <= -self.bounds_tol] = np.char.add(
            codes[lb_error <= -self.bounds_tol], "l")
        codes[ub_error <= -self.bounds_tol] = np.char.add(
            codes[ub_error <= -self.bounds_tol], "u")
        codes[feasibility > self.feasibility_tol] = np.char.add(
            codes[feasibility > self.feasibility_tol], "e")

        return codes