def stats(self, input_filepath):
        '''Display time domain statistical information about the audio
        channels. Audio is passed unmodified through the SoX processing chain.
        Statistics are calculated and displayed for each audio channel

        Unlike other Transformer methods, this does not modify the transformer
        effects chain. Instead it computes statistics on the output file that
        would be created if the build command were invoked.

        Note: The file is downmixed to mono prior to computation.

        Parameters
        ----------
        input_filepath : str
            Path to input file to compute stats on.

        Returns
        -------
        stats_dict : dict
            List of frequency (Hz), amplitude pairs.

        See Also
        --------
        stat, sox.file_info
        '''
        effect_args = ['channels', '1', 'stats']

        _, _, stats_output = self.build(
            input_filepath, None, extra_args=effect_args, return_output=True
        )

        stats_dict = {}
        lines = stats_output.split('\n')
        for line in lines:
            split_line = line.split()
            if len(split_line) == 0:
                continue
            value = split_line[-1]
            key = ' '.join(split_line[:-1])
            stats_dict[key] = value

        return stats_dict