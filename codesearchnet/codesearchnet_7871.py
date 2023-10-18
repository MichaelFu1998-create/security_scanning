def swap(self):
        '''Swap stereo channels. If the input is not stereo, pairs of channels
        are swapped, and a possible odd last channel passed through.

        E.g., for seven channels, the output order will be 2, 1, 4, 3, 6, 5, 7.

        See Also
        ----------
        remix

        '''
        effect_args = ['swap']
        self.effects.extend(effect_args)
        self.effects_log.append('swap')

        return self