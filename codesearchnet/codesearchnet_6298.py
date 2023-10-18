def _populate_solver(self, reaction_list, metabolite_list=None):
        """Populate attached solver with constraints and variables that
        model the provided reactions.
        """
        constraint_terms = AutoVivification()
        to_add = []
        if metabolite_list is not None:
            for met in metabolite_list:
                to_add += [self.problem.Constraint(
                    Zero, name=met.id, lb=0, ub=0)]
        self.add_cons_vars(to_add)

        for reaction in reaction_list:
            if reaction.id not in self.variables:
                forward_variable = self.problem.Variable(reaction.id)
                reverse_variable = self.problem.Variable(reaction.reverse_id)
                self.add_cons_vars([forward_variable, reverse_variable])
            else:
                reaction = self.reactions.get_by_id(reaction.id)
                forward_variable = reaction.forward_variable
                reverse_variable = reaction.reverse_variable
            for metabolite, coeff in six.iteritems(reaction.metabolites):
                if metabolite.id in self.constraints:
                    constraint = self.constraints[metabolite.id]
                else:
                    constraint = self.problem.Constraint(
                        Zero,
                        name=metabolite.id,
                        lb=0, ub=0)
                    self.add_cons_vars(constraint, sloppy=True)
                constraint_terms[constraint][forward_variable] = coeff
                constraint_terms[constraint][reverse_variable] = -coeff

        self.solver.update()
        for reaction in reaction_list:
            reaction = self.reactions.get_by_id(reaction.id)
            reaction.update_variable_bounds()
        for constraint, terms in six.iteritems(constraint_terms):
            constraint.set_linear_coefficients(terms)