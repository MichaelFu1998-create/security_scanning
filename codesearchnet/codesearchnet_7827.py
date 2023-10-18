def allpass(self, frequency, width_q=2.0):
        '''Apply a two-pole all-pass filter. An all-pass filter changes the
        audio’s frequency to phase relationship without changing its frequency
        to amplitude relationship. The filter is described in detail in at
        http://musicdsp.org/files/Audio-EQ-Cookbook.txt

        Parameters
        ----------
        frequency : float
            The filter's center frequency in Hz.
        width_q : float, default=2.0
            The filter's width as a Q-factor.

        See Also
        --------
        equalizer, highpass, lowpass, sinc

        '''
        if not is_number(frequency) or frequency <= 0:
            raise ValueError("frequency must be a positive number.")

        if not is_number(width_q) or width_q <= 0:
            raise ValueError("width_q must be a positive number.")

        effect_args = [
            'allpass', '{:f}'.format(frequency), '{:f}q'.format(width_q)
        ]

        self.effects.extend(effect_args)
        self.effects_log.append('allpass')
        return self