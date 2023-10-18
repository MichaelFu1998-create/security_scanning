def downsample(self, factor=2):
        '''Downsample the signal by an integer factor. Only the first out of
        each factor samples is retained, the others are discarded.

        No decimation filter is applied. If the input is not a properly
        bandlimited baseband signal, aliasing will occur. This may be desirable
        e.g., for frequency translation.

        For a general resampling effect with anti-aliasing, see rate.

        Parameters
        ----------
        factor : int, default=2
            Downsampling factor.

        See Also
        --------
        rate, upsample

        '''
        if not isinstance(factor, int) or factor < 1:
            raise ValueError('factor must be a positive integer.')

        effect_args = ['downsample', '{}'.format(factor)]

        self.effects.extend(effect_args)
        self.effects_log.append('downsample')
        return self