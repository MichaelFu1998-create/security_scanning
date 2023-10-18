def repair(self, rebuild_index=True, rebuild_relationships=True):
        """Update all indexes and pointers in a model

        Parameters
        ----------
        rebuild_index : bool
            rebuild the indices kept in reactions, metabolites and genes
        rebuild_relationships : bool
             reset all associations between genes, metabolites, model and
             then re-add them.
        """
        if rebuild_index:  # DictList indexes
            self.reactions._generate_index()
            self.metabolites._generate_index()
            self.genes._generate_index()
            self.groups._generate_index()
        if rebuild_relationships:
            for met in self.metabolites:
                met._reaction.clear()
            for gene in self.genes:
                gene._reaction.clear()
            for rxn in self.reactions:
                for met in rxn._metabolites:
                    met._reaction.add(rxn)
                for gene in rxn._genes:
                    gene._reaction.add(rxn)

        # point _model to self
        for l in (self.reactions, self.genes, self.metabolites, self.groups):
            for e in l:
                e._model = self