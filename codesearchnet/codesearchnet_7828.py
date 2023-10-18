def bandpass(self, frequency, width_q=2.0, constant_skirt=False):
        '''Apply a two-pole Butterworth band-pass filter with the given central
        frequency, and (3dB-point) band-width. The filter rolls off at 6dB per
        octave (20dB per decade) and is described in detail in
        http://musicdsp.org/files/Audio-EQ-Cookbook.txt

        Parameters
        ----------
        frequency : float
            The filter's center frequency in Hz.
        width_q : float, default=2.0
            The filter's width as a Q-factor.
        constant_skirt : bool, default=False
            If True, selects constant skirt gain (peak gain = width_q).
            If False, selects constant 0dB peak gain.

        See Also
        --------
        bandreject, sinc

        '''
        if not is_number(frequency) or frequency <= 0:
            raise ValueError("frequency must be a positive number.")

        if not is_number(width_q) or width_q <= 0:
            raise ValueError("width_q must be a positive number.")

        if not isinstance(constant_skirt, bool):
            raise ValueError("constant_skirt must be a boolean.")

        effect_args = ['bandpass']

        if constant_skirt:
            effect_args.append('-c')

        effect_args.extend(['{:f}'.format(frequency), '{:f}q'.format(width_q)])

        self.effects.extend(effect_args)
        self.effects_log.append('bandpass')
        return self