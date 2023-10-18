def add_metabolites(self, metabolites_to_add, combine=True,
                        reversibly=True):
        """Add metabolites and stoichiometric coefficients to the reaction.
        If the final coefficient for a metabolite is 0 then it is removed
        from the reaction.

        The change is reverted upon exit when using the model as a context.

        Parameters
        ----------
        metabolites_to_add : dict
            Dictionary with metabolite objects or metabolite identifiers as
            keys and coefficients as values. If keys are strings (name of a
            metabolite) the reaction must already be part of a model and a
            metabolite with the given name must exist in the model.

        combine : bool
            Describes behavior a metabolite already exists in the reaction.
            True causes the coefficients to be added.
            False causes the coefficient to be replaced.

        reversibly : bool
            Whether to add the change to the context to make the change
            reversibly or not (primarily intended for internal use).

        """
        old_coefficients = self.metabolites
        new_metabolites = []
        _id_to_metabolites = dict([(x.id, x) for x in self._metabolites])

        for metabolite, coefficient in iteritems(metabolites_to_add):

            # Make sure metabolites being added belong to the same model, or
            # else copy them.
            if isinstance(metabolite, Metabolite):
                if ((metabolite.model is not None) and
                        (metabolite.model is not self._model)):
                    metabolite = metabolite.copy()

            met_id = str(metabolite)
            # If a metabolite already exists in the reaction then
            # just add them.
            if met_id in _id_to_metabolites:
                reaction_metabolite = _id_to_metabolites[met_id]
                if combine:
                    self._metabolites[reaction_metabolite] += coefficient
                else:
                    self._metabolites[reaction_metabolite] = coefficient
            else:
                # If the reaction is in a model, ensure we aren't using
                # a duplicate metabolite.
                if self._model:
                    try:
                        metabolite = \
                            self._model.metabolites.get_by_id(met_id)
                    except KeyError as e:
                        if isinstance(metabolite, Metabolite):
                            new_metabolites.append(metabolite)
                        else:
                            # do we want to handle creation here?
                            raise e
                elif isinstance(metabolite, string_types):
                    # if we want to handle creation, this should be changed
                    raise ValueError("Reaction '%s' does not belong to a "
                                     "model. Either add the reaction to a "
                                     "model or use Metabolite objects instead "
                                     "of strings as keys."
                                     % self.id)
                self._metabolites[metabolite] = coefficient
                # make the metabolite aware that it is involved in this
                # reaction
                metabolite._reaction.add(self)

        # from cameo ...
        model = self.model
        if model is not None:
            model.add_metabolites(new_metabolites)

            for metabolite, coefficient in self._metabolites.items():
                model.constraints[
                    metabolite.id].set_linear_coefficients(
                    {self.forward_variable: coefficient,
                     self.reverse_variable: -coefficient
                     })

        for metabolite, the_coefficient in list(self._metabolites.items()):
            if the_coefficient == 0:
                # make the metabolite aware that it no longer participates
                # in this reaction
                metabolite._reaction.remove(self)
                self._metabolites.pop(metabolite)

        context = get_context(self)
        if context and reversibly:
            if combine:
                # Just subtract the metabolites that were added
                context(partial(
                    self.subtract_metabolites, metabolites_to_add,
                    combine=True, reversibly=False))
            else:
                # Reset them with add_metabolites
                mets_to_reset = {
                    key: old_coefficients[model.metabolites.get_by_any(key)[0]]
                    for key in iterkeys(metabolites_to_add)}

                context(partial(
                    self.add_metabolites, mets_to_reset,
                    combine=False, reversibly=False))