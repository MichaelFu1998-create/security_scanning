def stretch(self, factor, window=20):
        '''Change the audio duration (but not its pitch).
        **Unless factor is close to 1, use the tempo effect instead.**

        This effect is broadly equivalent to the tempo effect with search set
        to zero, so in general, its results are comparatively poor; it is
        retained as it can sometimes out-perform tempo for small factors.

        Parameters
        ----------
        factor : float
            The ratio of the new tempo to the old tempo.
            For ex. 1.1 speeds up the tempo by 10%; 0.9 slows it down by 10%.
            Note - this argument is the inverse of what is passed to the sox
            stretch effect for consistency with tempo.
        window : float, default=20
            Window size in miliseconds

        See Also
        --------
        tempo, speed, pitch

        '''
        if not is_number(factor) or factor <= 0:
            raise ValueError("factor must be a positive number")

        if factor < 0.5 or factor > 2:
            logger.warning(
                "Using an extreme time stretching factor. "
                "Quality of results will be poor"
            )

        if abs(factor - 1.0) > 0.1:
            logger.warning(
                "For this stretch factor, "
                "the tempo effect has better performance."
            )

        if not is_number(window) or window <= 0:
            raise ValueError(
                "window must be a positive number."
            )

        effect_args = ['stretch', '{:f}'.format(factor), '{:f}'.format(window)]

        self.effects.extend(effect_args)
        self.effects_log.append('stretch')

        return self