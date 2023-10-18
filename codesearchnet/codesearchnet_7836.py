def dcshift(self, shift=0.0):
        '''Apply a DC shift to the audio.

        Parameters
        ----------
        shift : float
            Amount to shift audio between -2 and 2. (Audio is between -1 and 1)

        See Also
        --------
        highpass

        '''
        if not is_number(shift) or shift < -2 or shift > 2:
            raise ValueError('shift must be a number between -2 and 2.')

        effect_args = ['dcshift', '{:f}'.format(shift)]

        self.effects.extend(effect_args)
        self.effects_log.append('dcshift')
        return self