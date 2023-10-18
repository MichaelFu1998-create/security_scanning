def update_costs(self):
        """Update the coefficients for the indicator variables in the objective.

        Done incrementally so that second time the function is called,
        active indicators in the current solutions gets higher cost than the
        unused indicators.
        """
        for var in self.indicators:
            if var not in self.costs:
                self.costs[var] = var.cost
            else:
                if var._get_primal() > self.integer_threshold:
                    self.costs[var] += var.cost
        self.model.objective.set_linear_coefficients(self.costs)