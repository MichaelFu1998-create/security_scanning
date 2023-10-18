def functional(self):
        """All required enzymes for reaction are functional.

        Returns
        -------
        bool
            True if the gene-protein-reaction (GPR) rule is fulfilled for
            this reaction, or if reaction is not associated to a model,
            otherwise False.
        """
        if self._model:
            tree, _ = parse_gpr(self.gene_reaction_rule)
            return eval_gpr(tree, {gene.id for gene in self.genes if
                                   not gene.functional})
        return True