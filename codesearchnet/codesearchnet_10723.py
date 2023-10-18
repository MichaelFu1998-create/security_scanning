def constant_light_profiles(self):
        """
        Returns
        -------
        light_profiles: [light_profiles.LightProfile]
            Light profiles with set variables
        """
        return [value for value in self.__dict__.values() if galaxy.is_light_profile(value)]