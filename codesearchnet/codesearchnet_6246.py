def _bounds_dist(self, p):
        """Get the lower and upper bound distances. Negative is bad."""

        prob = self.problem
        lb_dist = (p - prob.variable_bounds[0, ]).min()
        ub_dist = (prob.variable_bounds[1, ] - p).min()

        if prob.bounds.shape[0] > 0:
            const = prob.inequalities.dot(p)
            const_lb_dist = (const - prob.bounds[0, ]).min()
            const_ub_dist = (prob.bounds[1, ] - const).min()
            lb_dist = min(lb_dist, const_lb_dist)
            ub_dist = min(ub_dist, const_ub_dist)

        return np.array([lb_dist, ub_dist])