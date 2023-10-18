def speed(self, factor):
        '''Adjust the audio speed (pitch and tempo together).

        Technically, the speed effect only changes the sample rate information,
        leaving the samples themselves untouched. The rate effect is invoked
        automatically to resample to the output sample rate, using its default
        quality/speed. For higher quality or higher speed resampling, in
        addition to the speed effect, specify the rate effect with the desired
        quality option.

        Parameters
        ----------
        factor : float
            The ratio of the new speed to the old speed.
            For ex. 1.1 speeds up the audio by 10%; 0.9 slows it down by 10%.
            Note - this argument is the inverse of what is passed to the sox
            stretch effect for consistency with speed.

        See Also
        --------
        rate, tempo, pitch
        '''
        if not is_number(factor) or factor <= 0:
            raise ValueError("factor must be a positive number")

        if factor < 0.5 or factor > 2:
            logger.warning(
                "Using an extreme factor. Quality of results will be poor"
            )

        effect_args = ['speed', '{:f}'.format(factor)]

        self.effects.extend(effect_args)
        self.effects_log.append('speed')

        return self