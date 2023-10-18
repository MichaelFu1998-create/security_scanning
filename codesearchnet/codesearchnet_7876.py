def vad(self, location=1, normalize=True, activity_threshold=7.0,
            min_activity_duration=0.25, initial_search_buffer=1.0,
            max_gap=0.25, initial_pad=0.0):
        '''Voice Activity Detector. Attempts to trim silence and quiet
        background sounds from the ends of recordings of speech. The algorithm
        currently uses a simple cepstral power measurement to detect voice, so
        may be fooled by other things, especially music.

        The effect can trim only from the front of the audio, so in order to
        trim from the back, the reverse effect must also be used.

        Parameters
        ----------
        location : 1 or -1, default=1
            If 1, trims silence from the beginning
            If -1, trims silence from the end
        normalize : bool, default=True
            If true, normalizes audio before processing.
        activity_threshold : float, default=7.0
            The measurement level used to trigger activity detection. This may
            need to be cahnged depending on the noise level, signal level, and
            other characteristics of the input audio.
        min_activity_duration : float, default=0.25
            The time constant (in seconds) used to help ignore short bursts of
            sound.
        initial_search_buffer : float, default=1.0
            The amount of audio (in seconds) to search for quieter/shorter
            bursts of audio to include prior to the detected trigger point.
        max_gap : float, default=0.25
            The allowed gap (in seconds) between quiteter/shorter bursts of
            audio to include prior to the detected trigger point
        initial_pad : float, default=0.0
            The amount of audio (in seconds) to preserve before the trigger
            point and any found quieter/shorter bursts.

        See Also
        --------
        silence

        Examples
        --------
        >>> tfm = sox.Transformer()

        Remove silence from the beginning of speech

        >>> tfm.vad(initial_pad=0.3)

        Remove silence from the end of speech

        >>> tfm.vad(location=-1, initial_pad=0.2)

        '''
        if location not in [-1, 1]:
            raise ValueError("location must be -1 or 1.")
        if not isinstance(normalize, bool):
            raise ValueError("normalize muse be a boolean.")
        if not is_number(activity_threshold):
            raise ValueError("activity_threshold must be a number.")
        if not is_number(min_activity_duration) or min_activity_duration < 0:
            raise ValueError("min_activity_duration must be a positive number")
        if not is_number(initial_search_buffer) or initial_search_buffer < 0:
            raise ValueError("initial_search_buffer must be a positive number")
        if not is_number(max_gap) or max_gap < 0:
            raise ValueError("max_gap must be a positive number.")
        if not is_number(initial_pad) or initial_pad < 0:
            raise ValueError("initial_pad must be a positive number.")

        effect_args = []

        if normalize:
            effect_args.append('norm')

        if location == -1:
            effect_args.append('reverse')

        effect_args.extend([
            'vad',
            '-t', '{:f}'.format(activity_threshold),
            '-T', '{:f}'.format(min_activity_duration),
            '-s', '{:f}'.format(initial_search_buffer),
            '-g', '{:f}'.format(max_gap),
            '-p', '{:f}'.format(initial_pad)
        ])

        if location == -1:
            effect_args.append('reverse')

        self.effects.extend(effect_args)
        self.effects_log.append('vad')

        return self