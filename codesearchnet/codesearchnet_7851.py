def noiseprof(self, input_filepath, profile_path):
        '''Calculate a profile of the audio for use in noise reduction.
        Running this command does not effect the Transformer effects
        chain. When this function is called, the calculated noise profile
        file is saved to the `profile_path`.

        Parameters
        ----------
        input_filepath : str
            Path to audiofile from which to compute a noise profile.
        profile_path : str
            Path to save the noise profile file.

        See Also
        --------
        noisered

        '''
        if os.path.isdir(profile_path):
            raise ValueError(
                "profile_path {} is a directory.".format(profile_path))

        if os.path.dirname(profile_path) == '' and profile_path != '':
            _abs_profile_path = os.path.join(os.getcwd(), profile_path)
        else:
            _abs_profile_path = profile_path

        if not os.access(os.path.dirname(_abs_profile_path), os.W_OK):
            raise IOError(
                "profile_path {} is not writeable.".format(_abs_profile_path))

        effect_args = ['noiseprof', profile_path]
        self.build(input_filepath, None, extra_args=effect_args)

        return None