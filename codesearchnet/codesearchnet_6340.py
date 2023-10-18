def subtract_metabolites(self, metabolites, combine=True, reversibly=True):
        """Subtract metabolites from a reaction.

        That means add the metabolites with -1*coefficient. If the final
        coefficient for a metabolite is 0 then the metabolite is removed from
        the reaction.

        Notes
        -----
        * A final coefficient < 0 implies a reactant.
        * The change is reverted upon exit when using the model as a context.

        Parameters
        ----------
        metabolites : dict
            Dictionary where the keys are of class Metabolite and the values
            are the coefficients. These metabolites will be added to the
            reaction.

        combine : bool
            Describes behavior a metabolite already exists in the reaction.
            True causes the coefficients to be added.
            False causes the coefficient to be replaced.

        reversibly : bool
            Whether to add the change to the context to make the change
            reversibly or not (primarily intended for internal use).

        """
        self.add_metabolites({
            k: -v for k, v in iteritems(metabolites)},
            combine=combine, reversibly=reversibly)