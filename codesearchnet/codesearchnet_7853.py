def norm(self, db_level=-3.0):
        '''Normalize an audio file to a particular db level.
        This behaves identically to the gain effect with normalize=True.

        Parameters
        ----------
        db_level : float, default=-3.0
            Output volume (db)

        See Also
        --------
        gain, loudness

        '''
        if not is_number(db_level):
            raise ValueError('db_level must be a number.')

        effect_args = [
            'norm',
            '{:f}'.format(db_level)
        ]
        self.effects.extend(effect_args)
        self.effects_log.append('norm')

        return self