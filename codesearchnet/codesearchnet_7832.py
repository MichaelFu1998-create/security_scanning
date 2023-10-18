def chorus(self, gain_in=0.5, gain_out=0.9, n_voices=3, delays=None,
               decays=None, speeds=None, depths=None, shapes=None):
        '''Add a chorus effect to the audio. This can makeasingle vocal sound
        like a chorus, but can also be applied to instrumentation.

        Chorus resembles an echo effect with a short delay, but whereas with
        echo the delay is constant, with chorus, it is varied using sinusoidal
        or triangular modulation. The modulation depth defines the range the
        modulated delay is played before or after the delay. Hence the delayed
        sound will sound slower or faster, that is the delayed sound tuned
        around the original one, like in a chorus where some vocals are
        slightly off key.

        Parameters
        ----------
        gain_in : float, default=0.3
            The time in seconds over which the instantaneous level of the input
            signal is averaged to determine increases in volume.
        gain_out : float, default=0.8
            The time in seconds over which the instantaneous level of the input
            signal is averaged to determine decreases in volume.
        n_voices : int, default=3
            The number of voices in the chorus effect.
        delays : list of floats > 20 or None, default=None
            If a list, the list of delays (in miliseconds) of length n_voices.
            If None, the individual delay parameters are chosen automatically
            to be between 40 and 60 miliseconds.
        decays : list of floats or None, default=None
            If a list, the list of decays (as a fraction of gain_in) of length
            n_voices.
            If None, the individual decay parameters are chosen automatically
            to be between 0.3 and 0.4.
        speeds : list of floats or None, default=None
            If a list, the list of modulation speeds (in Hz) of length n_voices
            If None, the individual speed parameters are chosen automatically
            to be between 0.25 and 0.4 Hz.
        depths : list of floats or None, default=None
            If a list, the list of depths (in miliseconds) of length n_voices.
            If None, the individual delay parameters are chosen automatically
            to be between 1 and 3 miliseconds.
        shapes : list of 's' or 't' or None, deault=None
            If a list, the list of modulation shapes - 's' for sinusoidal or
            't' for triangular - of length n_voices.
            If None, the individual shapes are chosen automatically.

        '''
        if not is_number(gain_in) or gain_in <= 0 or gain_in > 1:
            raise ValueError("gain_in must be a number between 0 and 1.")
        if not is_number(gain_out) or gain_out <= 0 or gain_out > 1:
            raise ValueError("gain_out must be a number between 0 and 1.")
        if not isinstance(n_voices, int) or n_voices <= 0:
            raise ValueError("n_voices must be a positive integer.")

        # validate delays
        if not (delays is None or isinstance(delays, list)):
            raise ValueError("delays must be a list or None")
        if delays is not None:
            if len(delays) != n_voices:
                raise ValueError("the length of delays must equal n_voices")
            if any((not is_number(p) or p < 20) for p in delays):
                raise ValueError("the elements of delays must be numbers > 20")
        else:
            delays = [random.uniform(40, 60) for _ in range(n_voices)]

        # validate decays
        if not (decays is None or isinstance(decays, list)):
            raise ValueError("decays must be a list or None")
        if decays is not None:
            if len(decays) != n_voices:
                raise ValueError("the length of decays must equal n_voices")
            if any((not is_number(p) or p <= 0 or p > 1) for p in decays):
                raise ValueError(
                    "the elements of decays must be between 0 and 1"
                )
        else:
            decays = [random.uniform(0.3, 0.4) for _ in range(n_voices)]

        # validate speeds
        if not (speeds is None or isinstance(speeds, list)):
            raise ValueError("speeds must be a list or None")
        if speeds is not None:
            if len(speeds) != n_voices:
                raise ValueError("the length of speeds must equal n_voices")
            if any((not is_number(p) or p <= 0) for p in speeds):
                raise ValueError("the elements of speeds must be numbers > 0")
        else:
            speeds = [random.uniform(0.25, 0.4) for _ in range(n_voices)]

        # validate depths
        if not (depths is None or isinstance(depths, list)):
            raise ValueError("depths must be a list or None")
        if depths is not None:
            if len(depths) != n_voices:
                raise ValueError("the length of depths must equal n_voices")
            if any((not is_number(p) or p <= 0) for p in depths):
                raise ValueError("the elements of depths must be numbers > 0")
        else:
            depths = [random.uniform(1.0, 3.0) for _ in range(n_voices)]

        # validate shapes
        if not (shapes is None or isinstance(shapes, list)):
            raise ValueError("shapes must be a list or None")
        if shapes is not None:
            if len(shapes) != n_voices:
                raise ValueError("the length of shapes must equal n_voices")
            if any((p not in ['t', 's']) for p in shapes):
                raise ValueError("the elements of shapes must be 's' or 't'")
        else:
            shapes = [random.choice(['t', 's']) for _ in range(n_voices)]

        effect_args = ['chorus', '{}'.format(gain_in), '{}'.format(gain_out)]

        for i in range(n_voices):
            effect_args.extend([
                '{:f}'.format(delays[i]),
                '{:f}'.format(decays[i]),
                '{:f}'.format(speeds[i]),
                '{:f}'.format(depths[i]),
                '-{}'.format(shapes[i])
            ])

        self.effects.extend(effect_args)
        self.effects_log.append('chorus')
        return self