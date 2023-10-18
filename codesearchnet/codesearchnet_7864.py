def silence(self, location=0, silence_threshold=0.1,
                min_silence_duration=0.1, buffer_around_silence=False):
        '''Removes silent regions from an audio file.

        Parameters
        ----------
        location : int, default=0
            Where to remove silence. One of:
             * 0 to remove silence throughout the file (default),
             * 1 to remove silence from the beginning,
             * -1 to remove silence from the end,
        silence_threshold : float, default=0.1
            Silence threshold as percentage of maximum sample amplitude.
            Must be between 0 and 100.
        min_silence_duration : float, default=0.1
            The minimum ammount of time in seconds required for a region to be
            considered non-silent.
        buffer_around_silence : bool, default=False
            If True, leaves a buffer of min_silence_duration around removed
            silent regions.

        See Also
        --------
        vad

        '''
        if location not in [-1, 0, 1]:
            raise ValueError("location must be one of -1, 0, 1.")

        if not is_number(silence_threshold) or silence_threshold < 0:
            raise ValueError(
                "silence_threshold must be a number between 0 and 100"
            )
        elif silence_threshold >= 100:
            raise ValueError(
                "silence_threshold must be a number between 0 and 100"
            )

        if not is_number(min_silence_duration) or min_silence_duration <= 0:
            raise ValueError(
                "min_silence_duration must be a positive number."
            )

        if not isinstance(buffer_around_silence, bool):
            raise ValueError("buffer_around_silence must be a boolean.")

        effect_args = []

        if location == -1:
            effect_args.append('reverse')

        if buffer_around_silence:
            effect_args.extend(['silence', '-l'])
        else:
            effect_args.append('silence')

        effect_args.extend([
            '1',
            '{:f}'.format(min_silence_duration),
            '{:f}%'.format(silence_threshold)
        ])

        if location == 0:
            effect_args.extend([
                '-1',
                '{:f}'.format(min_silence_duration),
                '{:f}%'.format(silence_threshold)
            ])

        if location == -1:
            effect_args.append('reverse')

        self.effects.extend(effect_args)
        self.effects_log.append('silence')

        return self