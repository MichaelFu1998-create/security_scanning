def repeat(self, count=1):
        '''Repeat the entire audio count times.

        Parameters
        ----------
        count : int, default=1
            The number of times to repeat the audio.

        '''
        if not isinstance(count, int) or count < 1:
            raise ValueError("count must be a postive integer.")

        effect_args = ['repeat', '{}'.format(count)]
        self.effects.extend(effect_args)
        self.effects_log.append('repeat')