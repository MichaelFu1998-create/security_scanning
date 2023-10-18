def constant_mass_profiles(self):
        """
        Returns
        -------
        mass_profiles: [mass_profiles.MassProfile]
            Mass profiles with set variables
        """
        return [value for value in self.__dict__.values() if galaxy.is_mass_profile(value)]