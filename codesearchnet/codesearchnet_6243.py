def _reproject(self, p):
        """Reproject a point into the feasibility region.

        This function is guaranteed to return a new feasible point. However,
        no guarantees in terms of proximity to the original point can be made.

        Parameters
        ----------
        p : numpy.array
            The current sample point.

        Returns
        -------
        numpy.array
            A new feasible point. If `p` was feasible it wil return p.

        """

        nulls = self.problem.nullspace
        equalities = self.problem.equalities

        # don't reproject if point is feasible
        if np.allclose(equalities.dot(p), self.problem.b,
                       rtol=0, atol=self.feasibility_tol):
            new = p
        else:
            LOGGER.info("feasibility violated in sample"
                        " %d, trying to reproject" % self.n_samples)
            new = nulls.dot(nulls.T.dot(p))

        # Projections may violate bounds
        # set to random point in space in that case
        if any(new != p):
            LOGGER.info("reprojection failed in sample"
                        " %d, using random point in space" % self.n_samples)
            new = self._random_point()

        return new