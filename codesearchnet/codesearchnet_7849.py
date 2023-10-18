def loudness(self, gain_db=-10.0, reference_level=65.0):
        '''Loudness control. Similar to the gain effect, but provides
        equalisation for the human auditory system.

        The gain is adjusted by gain_db and the signal is equalised according
        to ISO 226 w.r.t. reference_level.

        Parameters
        ----------
        gain_db : float, default=-10.0
            Loudness adjustment amount (in dB)
        reference_level : float, default=65.0
            Reference level (in dB) according to which the signal is equalized.
            Must be between 50 and 75 (dB)

        See Also
        --------
        gain

        '''
        if not is_number(gain_db):
            raise ValueError('gain_db must be a number.')

        if not is_number(reference_level):
            raise ValueError('reference_level must be a number')

        if reference_level > 75 or reference_level < 50:
            raise ValueError('reference_level must be between 50 and 75')

        effect_args = [
            'loudness',
            '{:f}'.format(gain_db),
            '{:f}'.format(reference_level)
        ]
        self.effects.extend(effect_args)
        self.effects_log.append('loudness')

        return self