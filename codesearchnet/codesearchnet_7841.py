def echo(self, gain_in=0.8, gain_out=0.9, n_echos=1, delays=[60],
             decays=[0.4]):
        '''Add echoing to the audio.

        Echoes are reflected sound and can occur naturally amongst mountains
        (and sometimes large buildings) when talking or shouting; digital echo
        effects emulate this behav- iour and are often used to help fill out
        the sound of a single instrument or vocal. The time differ- ence
        between the original signal and the reflection is the 'delay' (time),
        and the loudness of the reflected signal is the 'decay'. Multiple
        echoes can have different delays and decays.

        Parameters
        ----------
        gain_in : float, default=0.8
            Input volume, between 0 and 1
        gain_out : float, default=0.9
            Output volume, between 0 and 1
        n_echos : int, default=1
            Number of reflections
        delays : list, default=[60]
            List of delays in miliseconds
        decays : list, default=[0.4]
            List of decays, relative to gain in between 0 and 1

        See Also
        --------
        echos, reverb, chorus
        '''
        if not is_number(gain_in) or gain_in <= 0 or gain_in > 1:
            raise ValueError("gain_in must be a number between 0 and 1.")

        if not is_number(gain_out) or gain_out <= 0 or gain_out > 1:
            raise ValueError("gain_out must be a number between 0 and 1.")

        if not isinstance(n_echos, int) or n_echos <= 0:
            raise ValueError("n_echos must be a positive integer.")

        # validate delays
        if not isinstance(delays, list):
            raise ValueError("delays must be a list")

        if len(delays) != n_echos:
            raise ValueError("the length of delays must equal n_echos")

        if any((not is_number(p) or p <= 0) for p in delays):
            raise ValueError("the elements of delays must be numbers > 0")

        # validate decays
        if not isinstance(decays, list):
            raise ValueError("decays must be a list")

        if len(decays) != n_echos:
            raise ValueError("the length of decays must equal n_echos")
        if any((not is_number(p) or p <= 0 or p > 1) for p in decays):
            raise ValueError(
                "the elements of decays must be between 0 and 1"
            )

        effect_args = ['echo', '{:f}'.format(gain_in), '{:f}'.format(gain_out)]

        for i in range(n_echos):
            effect_args.extend([
                '{}'.format(delays[i]),
                '{}'.format(decays[i])
            ])

        self.effects.extend(effect_args)
        self.effects_log.append('echo')
        return self