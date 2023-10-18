def _dissociate_gene(self, cobra_gene):
        """Dissociates a cobra.Gene object with a cobra.Reaction.

        Parameters
        ----------
        cobra_gene : cobra.core.Gene.Gene

        """
        self._genes.discard(cobra_gene)
        cobra_gene._reaction.discard(self)