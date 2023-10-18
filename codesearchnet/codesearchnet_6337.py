def copy(self):
        """Copy a reaction

        The referenced metabolites and genes are also copied.

        """
        # no references to model when copying
        model = self._model
        self._model = None
        for i in self._metabolites:
            i._model = None
        for i in self._genes:
            i._model = None
        # now we can copy
        new_reaction = deepcopy(self)
        # restore the references
        self._model = model
        for i in self._metabolites:
            i._model = model
        for i in self._genes:
            i._model = model
        return new_reaction