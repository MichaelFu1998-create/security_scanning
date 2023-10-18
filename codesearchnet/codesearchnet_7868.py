def power_spectrum(self, input_filepath):
        '''Calculates the power spectrum (4096 point DFT). This method
        internally invokes the stat command with the -freq option.

        Note: The file is downmixed to mono prior to computation.

        Parameters
        ----------
        input_filepath : str
            Path to input file to compute stats on.

        Returns
        -------
        power_spectrum : list
            List of frequency (Hz), amplitude pairs.

        See Also
        --------
        stat, stats, sox.file_info
        '''
        effect_args = ['channels', '1', 'stat', '-freq']

        _, _, stat_output = self.build(
            input_filepath, None, extra_args=effect_args, return_output=True
        )

        power_spectrum = []
        lines = stat_output.split('\n')
        for line in lines:
            split_line = line.split()
            if len(split_line) != 2:
                continue

            freq, amp = split_line
            power_spectrum.append([float(freq), float(amp)])

        return power_spectrum