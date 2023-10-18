def convert(self, samplerate=None, n_channels=None, bitdepth=None):
        '''Converts output audio to the specified format.

        Parameters
        ----------
        samplerate : float, default=None
            Desired samplerate. If None, defaults to the same as input.
        n_channels : int, default=None
            Desired number of channels. If None, defaults to the same as input.
        bitdepth : int, default=None
            Desired bitdepth. If None, defaults to the same as input.

        See Also
        --------
        rate

        '''
        bitdepths = [8, 16, 24, 32, 64]
        if bitdepth is not None:
            if bitdepth not in bitdepths:
                raise ValueError(
                    "bitdepth must be one of {}.".format(str(bitdepths))
                )
            self.output_format.extend(['-b', '{}'.format(bitdepth)])
        if n_channels is not None:
            if not isinstance(n_channels, int) or n_channels <= 0:
                raise ValueError(
                    "n_channels must be a positive integer."
                )
            self.output_format.extend(['-c', '{}'.format(n_channels)])
        if samplerate is not None:
            if not is_number(samplerate) or samplerate <= 0:
                raise ValueError("samplerate must be a positive number.")
            self.rate(samplerate)
        return self