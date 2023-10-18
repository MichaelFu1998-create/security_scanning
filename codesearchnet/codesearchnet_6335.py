def remove_from_model(self, remove_orphans=False):
        """Removes the reaction from a model.

        This removes all associations between a reaction the associated
        model, metabolites and genes.

        The change is reverted upon exit when using the model as a context.

        Parameters
        ----------
        remove_orphans : bool
            Remove orphaned genes and metabolites from the model as well

        """
        self._model.remove_reactions([self], remove_orphans=remove_orphans)