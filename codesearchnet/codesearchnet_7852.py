def noisered(self, profile_path, amount=0.5):
        '''Reduce noise in the audio signal by profiling and filtering.
        This effect is moderately effective at removing consistent
        background noise such as hiss or hum.

        Parameters
        ----------
        profile_path : str
            Path to a noise profile file.
            This file can be generated using the `noiseprof` effect.
        amount : float, default=0.5
            How much noise should be removed is specified by amount. Should
            be between 0 and 1.  Higher numbers will remove more noise but
            present a greater likelihood  of  removing wanted  components  of
            the  audio  signal.

        See Also
        --------
        noiseprof

        '''

        if not os.path.exists(profile_path):
            raise IOError(
                "profile_path {} does not exist.".format(profile_path))

        if not is_number(amount) or amount < 0 or amount > 1:
            raise ValueError("amount must be a number between 0 and 1.")

        effect_args = [
            'noisered',
            profile_path,
            '{:f}'.format(amount)
        ]
        self.effects.extend(effect_args)
        self.effects_log.append('noisered')

        return self