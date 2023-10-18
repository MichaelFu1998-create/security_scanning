def generate_fva_warmup(self):
        """Generate the warmup points for the sampler.

        Generates warmup points by setting each flux as the sole objective
        and minimizing/maximizing it. Also caches the projection of the
        warmup points into the nullspace for non-homogeneous problems (only
        if necessary).

        """

        self.n_warmup = 0
        reactions = self.model.reactions
        self.warmup = np.zeros((2 * len(reactions), len(self.model.variables)))
        self.model.objective = Zero

        for sense in ("min", "max"):
            self.model.objective_direction = sense

            for i, r in enumerate(reactions):
                variables = (self.model.variables[self.fwd_idx[i]],
                             self.model.variables[self.rev_idx[i]])

                # Omit fixed reactions if they are non-homogeneous
                if r.upper_bound - r.lower_bound < self.bounds_tol:
                    LOGGER.info("skipping fixed reaction %s" % r.id)
                    continue

                self.model.objective.set_linear_coefficients(
                    {variables[0]: 1, variables[1]: -1})

                self.model.slim_optimize()

                if not self.model.solver.status == OPTIMAL:
                    LOGGER.info("can not maximize reaction %s, skipping it" %
                                r.id)
                    continue

                primals = self.model.solver.primal_values
                sol = [primals[v.name] for v in self.model.variables]
                self.warmup[self.n_warmup, ] = sol
                self.n_warmup += 1

                # Reset objective
                self.model.objective.set_linear_coefficients(
                    {variables[0]: 0, variables[1]: 0})

        # Shrink to measure
        self.warmup = self.warmup[0:self.n_warmup, :]

        # Remove redundant search directions
        keep = np.logical_not(self._is_redundant(self.warmup))
        self.warmup = self.warmup[keep, :]
        self.n_warmup = self.warmup.shape[0]

        # Catch some special cases
        if len(self.warmup.shape) == 1 or self.warmup.shape[0] == 1:
            raise ValueError("Your flux cone consists only of a single point!")
        elif self.n_warmup == 2:
            if not self.problem.homogeneous:
                raise ValueError("Can not sample from an inhomogenous problem"
                                 " with only 2 search directions :(")
            LOGGER.info("All search directions on a line, adding another one.")
            newdir = self.warmup.T.dot([0.25, 0.25])
            self.warmup = np.vstack([self.warmup, newdir])
            self.n_warmup += 1

        # Shrink warmup points to measure
        self.warmup = shared_np_array(
            (self.n_warmup, len(self.model.variables)), self.warmup)