def biquad(self, b, a):
        '''Apply a biquad IIR filter with the given coefficients.

        Parameters
        ----------
        b : list of floats
            Numerator coefficients. Must be length 3
        a : list of floats
            Denominator coefficients. Must be length 3

        See Also
        --------
        fir, treble, bass, equalizer

        '''
        if not isinstance(b, list):
            raise ValueError('b must be a list.')

        if not isinstance(a, list):
            raise ValueError('a must be a list.')

        if len(b) != 3:
            raise ValueError('b must be a length 3 list.')

        if len(a) != 3:
            raise ValueError('a must be a length 3 list.')

        if not all([is_number(b_val) for b_val in b]):
            raise ValueError('all elements of b must be numbers.')

        if not all([is_number(a_val) for a_val in a]):
            raise ValueError('all elements of a must be numbers.')

        effect_args = [
            'biquad', '{:f}'.format(b[0]), '{:f}'.format(b[1]),
            '{:f}'.format(b[2]), '{:f}'.format(a[0]),
            '{:f}'.format(a[1]), '{:f}'.format(a[2])
        ]

        self.effects.extend(effect_args)
        self.effects_log.append('biquad')
        return self