def equalizer(self, frequency, width_q, gain_db):
        '''Apply a two-pole peaking equalisation (EQ) filter to boost or
        reduce around a given frequency.
        This effect can be applied multiple times to produce complex EQ curves.

        Parameters
        ----------
        frequency : float
            The filter's central frequency in Hz.
        width_q : float
            The filter's width as a Q-factor.
        gain_db : float
            The filter's gain in dB.

        See Also
        --------
        bass, treble

        '''
        if not is_number(frequency) or frequency <= 0:
            raise ValueError("frequency must be a positive number.")

        if not is_number(width_q) or width_q <= 0:
            raise ValueError("width_q must be a positive number.")

        if not is_number(gain_db):
            raise ValueError("gain_db must be a number.")

        effect_args = [
            'equalizer',
            '{:f}'.format(frequency),
            '{:f}q'.format(width_q),
            '{:f}'.format(gain_db)
        ]
        self.effects.extend(effect_args)
        self.effects_log.append('equalizer')
        return self