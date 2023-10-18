def get_coefficient(self, metabolite_id):
        """
        Return the stoichiometric coefficient of a metabolite.

        Parameters
        ----------
        metabolite_id : str or cobra.Metabolite

        """
        if isinstance(metabolite_id, Metabolite):
            return self._metabolites[metabolite_id]

        _id_to_metabolites = {m.id: m for m in self._metabolites}
        return self._metabolites[_id_to_metabolites[metabolite_id]]