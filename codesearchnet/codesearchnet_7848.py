def hilbert(self, num_taps=None):
        '''Apply an odd-tap Hilbert transform filter, phase-shifting the signal
        by 90 degrees. This is used in many matrix coding schemes and for
        analytic signal generation. The process is often written as a
        multiplication by i (or j), the imaginary unit. An odd-tap Hilbert
        transform filter has a bandpass characteristic, attenuating the lowest
        and highest frequencies.

        Parameters
        ----------
        num_taps : int or None, default=None
            Number of filter taps - must be odd. If none, it is chosen to have
            a cutoff frequency of about 75 Hz.

        '''
        if num_taps is not None and not isinstance(num_taps, int):
            raise ValueError("num taps must be None or an odd integer.")

        if num_taps is not None and num_taps % 2 == 0:
            raise ValueError("num_taps must an odd integer.")

        effect_args = ['hilbert']

        if num_taps is not None:
            effect_args.extend(['-n', '{}'.format(num_taps)])

        self.effects.extend(effect_args)
        self.effects_log.append('hilbert')

        return self