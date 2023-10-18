def overdrive(self, gain_db=20.0, colour=20.0):
        '''Apply non-linear distortion.

        Parameters
        ----------
        gain_db : float, default=20
            Controls the amount of distortion (dB).
        colour : float, default=20
            Controls the amount of even harmonic content in the output (dB).

        '''
        if not is_number(gain_db):
            raise ValueError('db_level must be a number.')

        if not is_number(colour):
            raise ValueError('colour must be a number.')

        effect_args = [
            'overdrive',
            '{:f}'.format(gain_db),
            '{:f}'.format(colour)
        ]
        self.effects.extend(effect_args)
        self.effects_log.append('overdrive')

        return self