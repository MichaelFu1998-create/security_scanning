def contrast(self, amount=75):
        '''Comparable with compression, this effect modifies an audio signal to
        make it sound louder.

        Parameters
        ----------
        amount : float
            Amount of enhancement between 0 and 100.

        See Also
        --------
        compand, mcompand

        '''
        if not is_number(amount) or amount < 0 or amount > 100:
            raise ValueError('amount must be a number between 0 and 100.')

        effect_args = ['contrast', '{:f}'.format(amount)]

        self.effects.extend(effect_args)
        self.effects_log.append('contrast')
        return self