def get(self, profile_id):
        '''Returns the profile with the received ID as a dict

        If a local copy of the profile exists, it'll be returned. If not, it'll
        be downloaded from the web. The results are cached, so any subsequent
        calls won't hit the filesystem or the web.

        Args:
            profile_id (str): The ID of the profile you want.

        Raises:
            RegistryError: If there was some problem opening the profile file
                or its format was incorrect.
        '''
        if profile_id not in self._profiles:
            try:
                self._profiles[profile_id] = self._get_profile(profile_id)
            except (ValueError,
                    IOError) as e:
                six.raise_from(RegistryError(e), e)
        return self._profiles[profile_id]