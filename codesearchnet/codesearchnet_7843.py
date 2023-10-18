def fade(self, fade_in_len=0.0, fade_out_len=0.0, fade_shape='q'):
        '''Add a fade in and/or fade out to an audio file.
        Default fade shape is 1/4 sine wave.

        Parameters
        ----------
        fade_in_len : float, default=0.0
            Length of fade-in (seconds). If fade_in_len = 0,
            no fade in is applied.
        fade_out_len : float, defaut=0.0
            Length of fade-out (seconds). If fade_out_len = 0,
            no fade in is applied.
        fade_shape : str, default='q'
            Shape of fade. Must be one of
             * 'q' for quarter sine (default),
             * 'h' for half sine,
             * 't' for linear,
             * 'l' for logarithmic
             * 'p' for inverted parabola.

        See Also
        --------
        splice

        '''
        fade_shapes = ['q', 'h', 't', 'l', 'p']
        if fade_shape not in fade_shapes:
            raise ValueError(
                "Fade shape must be one of {}".format(" ".join(fade_shapes))
            )
        if not is_number(fade_in_len) or fade_in_len < 0:
            raise ValueError("fade_in_len must be a nonnegative number.")
        if not is_number(fade_out_len) or fade_out_len < 0:
            raise ValueError("fade_out_len must be a nonnegative number.")

        effect_args = []

        if fade_in_len > 0:
            effect_args.extend([
                'fade', '{}'.format(fade_shape), '{:f}'.format(fade_in_len)
            ])

        if fade_out_len > 0:
            effect_args.extend([
                'reverse', 'fade', '{}'.format(fade_shape),
                '{:f}'.format(fade_out_len), 'reverse'
            ])

        if len(effect_args) > 0:
            self.effects.extend(effect_args)
            self.effects_log.append('fade')

        return self