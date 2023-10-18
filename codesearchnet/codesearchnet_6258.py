def add_switches_and_objective(self):
        """ Update gapfilling model with switches and the indicator objective.
        """
        constraints = list()
        big_m = max(max(abs(b) for b in r.bounds)
                    for r in self.model.reactions)
        prob = self.model.problem
        for rxn in self.model.reactions:
            if not hasattr(rxn, 'gapfilling_type'):
                continue
            indicator = prob.Variable(
                name='indicator_{}'.format(rxn.id), lb=0, ub=1, type='binary')
            if rxn.id in self.penalties:
                indicator.cost = self.penalties[rxn.id]
            else:
                indicator.cost = self.penalties[rxn.gapfilling_type]
            indicator.rxn_id = rxn.id
            self.indicators.append(indicator)

            # if z = 1 v_i is allowed non-zero
            # v_i - Mz <= 0   and   v_i + Mz >= 0
            constraint_lb = prob.Constraint(
                rxn.flux_expression - big_m * indicator, ub=0,
                name='constraint_lb_{}'.format(rxn.id), sloppy=True)
            constraint_ub = prob.Constraint(
                rxn.flux_expression + big_m * indicator, lb=0,
                name='constraint_ub_{}'.format(rxn.id), sloppy=True)

            constraints.extend([constraint_lb, constraint_ub])

        self.model.add_cons_vars(self.indicators)
        self.model.add_cons_vars(constraints, sloppy=True)
        self.model.objective = prob.Objective(
            Zero, direction='min', sloppy=True)
        self.model.objective.set_linear_coefficients({
            i: 1 for i in self.indicators})
        self.update_costs()