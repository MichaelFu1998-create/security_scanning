def gain(self, gain_db=0.0, normalize=True, limiter=False, balance=None):
        '''Apply amplification or attenuation to the audio signal.

        Parameters
        ----------
        gain_db : float, default=0.0
            Gain adjustment in decibels (dB).
        normalize : bool, default=True
            If True, audio is normalized to gain_db relative to full scale.
            If False, simply adjusts the audio power level by gain_db.
        limiter : bool, default=False
            If True, a simple limiter is invoked to prevent clipping.
        balance : str or None, default=None
            Balance gain across channels. Can be one of:
             * None applies no balancing (default)
             * 'e' applies gain to all channels other than that with the
                highest peak level, such that all channels attain the same
                peak level
             * 'B' applies gain to all channels other than that with the
                highest RMS level, such that all channels attain the same
                RMS level
             * 'b' applies gain with clipping protection to all channels other
                than that with the highest RMS level, such that all channels
                attain the same RMS level
            If normalize=True, 'B' and 'b' are equivalent.

        See Also
        --------
        loudness

        '''
        if not is_number(gain_db):
            raise ValueError("gain_db must be a number.")

        if not isinstance(normalize, bool):
            raise ValueError("normalize must be a boolean.")

        if not isinstance(limiter, bool):
            raise ValueError("limiter must be a boolean.")

        if balance not in [None, 'e', 'B', 'b']:
            raise ValueError("balance must be one of None, 'e', 'B', or 'b'.")

        effect_args = ['gain']

        if balance is not None:
            effect_args.append('-{}'.format(balance))

        if normalize:
            effect_args.append('-n')

        if limiter:
            effect_args.append('-l')

        effect_args.append('{:f}'.format(gain_db))
        self.effects.extend(effect_args)
        self.effects_log.append('gain')

        return self