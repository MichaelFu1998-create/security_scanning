def extend_model(self, exchange_reactions=False, demand_reactions=True):
        """Extend gapfilling model.

        Add reactions from universal model and optionally exchange and
        demand reactions for all metabolites in the model to perform
        gapfilling on.

        Parameters
        ----------
        exchange_reactions : bool
            Consider adding exchange (uptake) reactions for all metabolites
            in the model.
        demand_reactions : bool
            Consider adding demand reactions for all metabolites.
        """
        for rxn in self.universal.reactions:
            rxn.gapfilling_type = 'universal'
        new_metabolites = self.universal.metabolites.query(
            lambda metabolite: metabolite not in self.model.metabolites
                                                           )
        self.model.add_metabolites(new_metabolites)
        existing_exchanges = []
        for rxn in self.universal.boundary:
            existing_exchanges = existing_exchanges + \
                [met.id for met in list(rxn.metabolites)]

        for met in self.model.metabolites:
            if exchange_reactions:
                # check for exchange reaction in model already
                if met.id not in existing_exchanges:
                    rxn = self.universal.add_boundary(
                        met, type='exchange_smiley', lb=-1000, ub=0,
                        reaction_id='EX_{}'.format(met.id))
                    rxn.gapfilling_type = 'exchange'
            if demand_reactions:
                rxn = self.universal.add_boundary(
                    met, type='demand_smiley', lb=0, ub=1000,
                    reaction_id='DM_{}'.format(met.id))
                rxn.gapfilling_type = 'demand'

        new_reactions = self.universal.reactions.query(
            lambda reaction: reaction not in self.model.reactions
        )
        self.model.add_reactions(new_reactions)