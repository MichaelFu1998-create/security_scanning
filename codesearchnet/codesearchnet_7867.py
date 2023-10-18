def stat(self, input_filepath, scale=None, rms=False):
        '''Display time and frequency domain statistical information about the
        audio. Audio is passed unmodified through the SoX processing chain.

        Unlike other Transformer methods, this does not modify the transformer
        effects chain. Instead it computes statistics on the output file that
        would be created if the build command were invoked.

        Note: The file is downmixed to mono prior to computation.

        Parameters
        ----------
        input_filepath : str
            Path to input file to compute stats on.
        scale : float or None, default=None
            If not None, scales the input by the given scale factor.
        rms : bool, default=False
            If True, scales all values by the average rms amplitude.

        Returns
        -------
        stat_dict : dict
            Dictionary of statistics.

        See Also
        --------
        stats, power_spectrum, sox.file_info
        '''
        effect_args = ['channels', '1', 'stat']
        if scale is not None:
            if not is_number(scale) or scale <= 0:
                raise ValueError("scale must be a positive number.")
            effect_args.extend(['-s', '{:f}'.format(scale)])

        if rms:
            effect_args.append('-rms')

        _, _, stat_output = self.build(
            input_filepath, None, extra_args=effect_args, return_output=True
        )

        stat_dict = {}
        lines = stat_output.split('\n')
        for line in lines:
            split_line = line.split()
            if len(split_line) == 0:
                continue
            value = split_line[-1]
            key = ' '.join(split_line[:-1])
            stat_dict[key.strip(':')] = value

        return stat_dict