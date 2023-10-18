def delete(self, remove_orphans=False):
        """Removes the reaction from a model.

        This removes all associations between a reaction the associated
        model, metabolites and genes.

        The change is reverted upon exit when using the model as a context.

        Deprecated, use `reaction.remove_from_model` instead.

        Parameters
        ----------
        remove_orphans : bool
            Remove orphaned genes and metabolites from the model as well

        """
        warn("delete is deprecated. Use reaction.remove_from_model instead",
             DeprecationWarning)
        self.remove_from_model(remove_orphans=remove_orphans)