def pitch(self, n_semitones, quick=False):
        '''Pitch shift the audio without changing the tempo.

        This effect uses the WSOLA algorithm. The audio is chopped up into
        segments which are then shifted in the time domain and overlapped
        (cross-faded) at points where their waveforms are most similar as
        determined by measurement of least squares.

        Parameters
        ----------
        n_semitones : float
            The number of semitones to shift. Can be positive or negative.
        quick : bool, default=False
            If True, this effect will run faster but with lower sound quality.

        See Also
        --------
        bend, speed, tempo

        '''
        if not is_number(n_semitones):
            raise ValueError("n_semitones must be a positive number")

        if n_semitones < -12 or n_semitones > 12:
            logger.warning(
                "Using an extreme pitch shift. "
                "Quality of results will be poor"
            )

        if not isinstance(quick, bool):
            raise ValueError("quick must be a boolean.")

        effect_args = ['pitch']

        if quick:
            effect_args.append('-q')

        effect_args.append('{:f}'.format(n_semitones * 100.))

        self.effects.extend(effect_args)
        self.effects_log.append('pitch')

        return self