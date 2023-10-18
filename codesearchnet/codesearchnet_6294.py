def remove_reactions(self, reactions, remove_orphans=False):
        """Remove reactions from the model.

        The change is reverted upon exit when using the model as a context.

        Parameters
        ----------
        reactions : list
            A list with reactions (`cobra.Reaction`), or their id's, to remove

        remove_orphans : bool
            Remove orphaned genes and metabolites from the model as well

        """
        if isinstance(reactions, string_types) or hasattr(reactions, "id"):
            warn("need to pass in a list")
            reactions = [reactions]

        context = get_context(self)

        for reaction in reactions:

            # Make sure the reaction is in the model
            try:
                reaction = self.reactions[self.reactions.index(reaction)]
            except ValueError:
                warn('%s not in %s' % (reaction, self))

            else:
                forward = reaction.forward_variable
                reverse = reaction.reverse_variable

                if context:

                    obj_coef = reaction.objective_coefficient

                    if obj_coef != 0:
                        context(partial(
                            self.solver.objective.set_linear_coefficients,
                            {forward: obj_coef, reverse: -obj_coef}))

                    context(partial(self._populate_solver, [reaction]))
                    context(partial(setattr, reaction, '_model', self))
                    context(partial(self.reactions.add, reaction))

                self.remove_cons_vars([forward, reverse])
                self.reactions.remove(reaction)
                reaction._model = None

                for met in reaction._metabolites:
                    if reaction in met._reaction:
                        met._reaction.remove(reaction)
                        if context:
                            context(partial(met._reaction.add, reaction))
                        if remove_orphans and len(met._reaction) == 0:
                            self.remove_metabolites(met)

                for gene in reaction._genes:
                    if reaction in gene._reaction:
                        gene._reaction.remove(reaction)
                        if context:
                            context(partial(gene._reaction.add, reaction))

                        if remove_orphans and len(gene._reaction) == 0:
                            self.genes.remove(gene)
                            if context:
                                context(partial(self.genes.add, gene))

                # remove reference to the reaction in all groups
                associated_groups = self.get_associated_groups(reaction)
                for group in associated_groups:
                    group.remove_members(reaction)