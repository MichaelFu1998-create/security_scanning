def vol(self, gain, gain_type='amplitude', limiter_gain=None):
        '''Apply an amplification or an attenuation to the audio signal.

        Parameters
        ----------
        gain : float
            Interpreted according to the given `gain_type`.
            If `gain_type' = 'amplitude', `gain' is a positive amplitude ratio.
            If `gain_type' = 'power', `gain' is a power (voltage squared).
            If `gain_type' = 'db', `gain' is in decibels.
        gain_type : string, default='amplitude'
            Type of gain. One of:
                - 'amplitude'
                - 'power'
                - 'db'
        limiter_gain : float or None, default=None
            If specified, a limiter is invoked on peaks greater than
            `limiter_gain' to prevent clipping.
            `limiter_gain` should be a positive value much less than 1.

        See Also
        --------
        gain, compand

        '''
        if not is_number(gain):
            raise ValueError('gain must be a number.')
        if limiter_gain is not None:
            if (not is_number(limiter_gain) or
                    limiter_gain <= 0 or limiter_gain >= 1):
                raise ValueError(
                    'limiter gain must be a positive number less than 1'
                )
        if gain_type in ['amplitude', 'power'] and gain < 0:
            raise ValueError(
                "If gain_type = amplitude or power, gain must be positive."
            )

        effect_args = ['vol']

        effect_args.append('{:f}'.format(gain))

        if gain_type == 'amplitude':
            effect_args.append('amplitude')
        elif gain_type == 'power':
            effect_args.append('power')
        elif gain_type == 'db':
            effect_args.append('dB')
        else:
            raise ValueError('gain_type must be one of amplitude power or db')

        if limiter_gain is not None:
            if gain_type in ['amplitude', 'power'] and gain > 1:
                effect_args.append('{:f}'.format(limiter_gain))
            elif gain_type == 'db' and gain > 0:
                effect_args.append('{:f}'.format(limiter_gain))

        self.effects.extend(effect_args)
        self.effects_log.append('vol')

        return self