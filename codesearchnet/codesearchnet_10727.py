def constant_profile_dict(self):
        """
        Returns
        -------
        constant_profile_dict: {str: geometry_profiles.GeometryProfile}
            A dictionary mapping_matrix instance variable names to profiles with set variables.
        """
        return {key: value for key, value in self.__dict__.items() if
                galaxy.is_light_profile(value) or galaxy.is_mass_profile(value)}