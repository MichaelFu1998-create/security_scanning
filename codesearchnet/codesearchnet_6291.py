def remove_metabolites(self, metabolite_list, destructive=False):
        """Remove a list of metabolites from the the object.

        The change is reverted upon exit when using the model as a context.

        Parameters
        ----------
        metabolite_list : list
            A list with `cobra.Metabolite` objects as elements.

        destructive : bool
            If False then the metabolite is removed from all
            associated reactions.  If True then all associated
            reactions are removed from the Model.

        """
        if not hasattr(metabolite_list, '__iter__'):
            metabolite_list = [metabolite_list]
        # Make sure metabolites exist in model
        metabolite_list = [x for x in metabolite_list
                           if x.id in self.metabolites]
        for x in metabolite_list:
            x._model = None

            # remove reference to the metabolite in all groups
            associated_groups = self.get_associated_groups(x)
            for group in associated_groups:
                group.remove_members(x)

            if not destructive:
                for the_reaction in list(x._reaction):
                    the_coefficient = the_reaction._metabolites[x]
                    the_reaction.subtract_metabolites({x: the_coefficient})

            else:
                for x in list(x._reaction):
                    x.remove_from_model()

        self.metabolites -= metabolite_list

        to_remove = [self.solver.constraints[m.id] for m in metabolite_list]
        self.remove_cons_vars(to_remove)

        context = get_context(self)
        if context:
            context(partial(self.metabolites.__iadd__, metabolite_list))
            for x in metabolite_list:
                context(partial(setattr, x, '_model', self))