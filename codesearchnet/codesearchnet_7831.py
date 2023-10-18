def channels(self, n_channels):
        '''Change the number of channels in the audio signal. If decreasing the
        number of channels it mixes channels together, if increasing the number
        of channels it duplicates.

        Note: This overrides arguments used in the convert effect!

        Parameters
        ----------
        n_channels : int
            Desired number of channels.

        See Also
        --------
        convert

        '''
        if not isinstance(n_channels, int) or n_channels <= 0:
            raise ValueError('n_channels must be a positive integer.')

        effect_args = ['channels', '{}'.format(n_channels)]

        self.effects.extend(effect_args)
        self.effects_log.append('channels')
        return self