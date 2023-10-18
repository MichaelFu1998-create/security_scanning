def gaussian_prior_model_for_arguments(self, arguments):
        """
        Create a new galaxy prior from a set of arguments, replacing the priors of some of this galaxy prior's prior
        models with new arguments.

        Parameters
        ----------
        arguments: dict
            A dictionary mapping_matrix between old priors and their replacements.

        Returns
        -------
        new_model: GalaxyModel
            A model with some or all priors replaced.
        """
        new_model = copy.deepcopy(self)

        for key, value in filter(lambda t: isinstance(t[1], pm.PriorModel), self.__dict__.items()):
            setattr(new_model, key, value.gaussian_prior_model_for_arguments(arguments))

        return new_model