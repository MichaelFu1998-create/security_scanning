def profile_prior_model_dict(self):
        """
        Returns
        -------
        profile_prior_model_dict: {str: PriorModel}
            A dictionary mapping_matrix instance variable names to variable profiles.
        """
        return {key: value for key, value in
                filter(lambda t: isinstance(t[1], pm.PriorModel) and is_profile_class(t[1].cls),
                       self.__dict__.items())}