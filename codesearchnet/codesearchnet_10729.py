def instance_for_arguments(self, arguments):
        """
        Create an instance of the associated class for a set of arguments

        Parameters
        ----------
        arguments: {Prior: value}
            Dictionary mapping_matrix priors to attribute analysis_path and value pairs

        Returns
        -------
            An instance of the class
        """
        profiles = {**{key: value.instance_for_arguments(arguments)
                       for key, value
                       in self.profile_prior_model_dict.items()}, **self.constant_profile_dict}

        try:
            redshift = self.redshift.instance_for_arguments(arguments)
        except AttributeError:
            redshift = self.redshift
        pixelization = self.pixelization.instance_for_arguments(arguments) \
            if isinstance(self.pixelization, pm.PriorModel) \
            else self.pixelization
        regularization = self.regularization.instance_for_arguments(arguments) \
            if isinstance(self.regularization, pm.PriorModel) \
            else self.regularization
        hyper_galaxy = self.hyper_galaxy.instance_for_arguments(arguments) \
            if isinstance(self.hyper_galaxy, pm.PriorModel) \
            else self.hyper_galaxy

        return galaxy.Galaxy(redshift=redshift, pixelization=pixelization, regularization=regularization,
                             hyper_galaxy=hyper_galaxy, **profiles)