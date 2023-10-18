def fir(self, coefficients):
        '''Use SoX’s FFT convolution engine with given FIR filter coefficients.

        Parameters
        ----------
        coefficients : list
            fir filter coefficients

        '''
        if not isinstance(coefficients, list):
            raise ValueError("coefficients must be a list.")

        if not all([is_number(c) for c in coefficients]):
            raise ValueError("coefficients must be numbers.")

        effect_args = ['fir']
        effect_args.extend(['{:f}'.format(c) for c in coefficients])

        self.effects.extend(effect_args)
        self.effects_log.append('fir')

        return self