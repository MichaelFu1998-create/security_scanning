def medium(self, medium):
        """Get or set the constraints on the model exchanges.

        `model.medium` returns a dictionary of the bounds for each of the
        boundary reactions, in the form of `{rxn_id: bound}`, where `bound`
        specifies the absolute value of the bound in direction of metabolite
        creation (i.e., lower_bound for `met <--`, upper_bound for `met -->`)

        Parameters
        ----------
        medium: dictionary-like
            The medium to initialize. medium should be a dictionary defining
            `{rxn_id: bound}` pairs.

        """

        def set_active_bound(reaction, bound):
            if reaction.reactants:
                reaction.lower_bound = -bound
            elif reaction.products:
                reaction.upper_bound = bound

        # Set the given media bounds
        media_rxns = list()
        exchange_rxns = frozenset(self.exchanges)
        for rxn_id, bound in iteritems(medium):
            rxn = self.reactions.get_by_id(rxn_id)
            if rxn not in exchange_rxns:
                LOGGER.warn("%s does not seem to be an"
                            " an exchange reaction. Applying bounds anyway.",
                            rxn.id)
            media_rxns.append(rxn)
            set_active_bound(rxn, bound)

        media_rxns = frozenset(media_rxns)

        # Turn off reactions not present in media
        for rxn in (exchange_rxns - media_rxns):
            set_active_bound(rxn, 0)