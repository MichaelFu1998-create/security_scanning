def highpass(self, frequency, width_q=0.707, n_poles=2):
        '''Apply a high-pass filter with 3dB point frequency. The filter can be
        either single-pole or double-pole. The filters roll off at 6dB per pole
        per octave (20dB per pole per decade).

        Parameters
        ----------
        frequency : float
            The filter's cutoff frequency in Hz.
        width_q : float, default=0.707
            The filter's width as a Q-factor. Applies only when n_poles=2.
            The default gives a Butterworth response.
        n_poles : int, default=2
            The number of poles in the filter. Must be either 1 or 2

        See Also
        --------
        lowpass, equalizer, sinc, allpass

        '''
        if not is_number(frequency) or frequency <= 0:
            raise ValueError("frequency must be a positive number.")

        if not is_number(width_q) or width_q <= 0:
            raise ValueError("width_q must be a positive number.")

        if n_poles not in [1, 2]:
            raise ValueError("n_poles must be 1 or 2.")

        effect_args = [
            'highpass', '-{}'.format(n_poles), '{:f}'.format(frequency)
        ]

        if n_poles == 2:
            effect_args.append('{:f}q'.format(width_q))

        self.effects.extend(effect_args)
        self.effects_log.append('highpass')

        return self