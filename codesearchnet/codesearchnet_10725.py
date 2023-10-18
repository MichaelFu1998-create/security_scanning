def prior_models(self):
        """
        Returns
        -------
        prior_models: [model_mapper.PriorModel]
            A list of the prior models (e.g. variable profiles) attached to this galaxy prior
        """
        return [value for _, value in
                filter(lambda t: isinstance(t[1], pm.PriorModel), self.__dict__.items())]