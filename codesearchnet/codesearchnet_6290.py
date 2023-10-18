def add_metabolites(self, metabolite_list):
        """Will add a list of metabolites to the model object and add new
        constraints accordingly.

        The change is reverted upon exit when using the model as a context.

        Parameters
        ----------
        metabolite_list : A list of `cobra.core.Metabolite` objects

        """
        if not hasattr(metabolite_list, '__iter__'):
            metabolite_list = [metabolite_list]
        if len(metabolite_list) == 0:
            return None

        # First check whether the metabolites exist in the model
        metabolite_list = [x for x in metabolite_list
                           if x.id not in self.metabolites]

        bad_ids = [m for m in metabolite_list
                   if not isinstance(m.id, string_types) or len(m.id) < 1]
        if len(bad_ids) != 0:
            raise ValueError('invalid identifiers in {}'.format(repr(bad_ids)))

        for x in metabolite_list:
            x._model = self
        self.metabolites += metabolite_list

        # from cameo ...
        to_add = []
        for met in metabolite_list:
            if met.id not in self.constraints:
                constraint = self.problem.Constraint(
                    Zero, name=met.id, lb=0, ub=0)
                to_add += [constraint]

        self.add_cons_vars(to_add)

        context = get_context(self)
        if context:
            context(partial(self.metabolites.__isub__, metabolite_list))
            for x in metabolite_list:
                # Do we care?
                context(partial(setattr, x, '_model', None))