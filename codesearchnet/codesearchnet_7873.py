def treble(self, gain_db, frequency=3000.0, slope=0.5):
        '''Boost or cut the treble (lower) frequencies of the audio using a
        two-pole shelving filter with a response similar to that of a standard
        hi-fi’s tone-controls. This is also known as shelving equalisation.

        The filters are described in detail in
        http://musicdsp.org/files/Audio-EQ-Cookbook.txt

        Parameters
        ----------
        gain_db : float
            The gain at the Nyquist frequency.
            For a large cut use -20, for a large boost use 20.
        frequency : float, default=100.0
            The filter's cutoff frequency in Hz.
        slope : float, default=0.5
            The steepness of the filter's shelf transition.
            For a gentle slope use 0.3, and use 1.0 for a steep slope.

        See Also
        --------
        bass, equalizer

        '''
        if not is_number(gain_db):
            raise ValueError("gain_db must be a number")

        if not is_number(frequency) or frequency <= 0:
            raise ValueError("frequency must be a positive number.")

        if not is_number(slope) or slope <= 0 or slope > 1.0:
            raise ValueError("width_q must be a positive number.")

        effect_args = [
            'treble', '{:f}'.format(gain_db), '{:f}'.format(frequency),
            '{:f}s'.format(slope)
        ]

        self.effects.extend(effect_args)
        self.effects_log.append('treble')

        return self