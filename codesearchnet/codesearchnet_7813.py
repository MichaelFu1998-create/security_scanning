def preview(self, input_filepath_list, combine_type, input_volumes=None):
        '''Play a preview of the output with the current set of effects

        Parameters
        ----------
        input_filepath_list : list of str
            List of paths to input audio files.
        combine_type : str
            Input file combining method. One of the following values:
                * concatenate : combine input files by concatenating in the
                    order given.
                * merge : combine input files by stacking each input file into
                    a new channel of the output file.
                * mix : combine input files by summing samples in corresponding
                    channels.
                * mix-power : combine input files with volume adjustments such
                    that the output volume is roughly equivlent to one of the
                    input signals.
                * multiply : combine input files by multiplying samples in
                    corresponding samples.
        input_volumes : list of float, default=None
            List of volumes to be applied upon combining input files. Volumes
            are applied to the input files in order.
            If None, input files will be combined at their original volumes.

        '''
        args = ["play", "--no-show-progress"]
        args.extend(self.globals)
        args.extend(['--combine', combine_type])

        input_format_list = _build_input_format_list(
            input_filepath_list, input_volumes, self.input_format
        )
        input_args = _build_input_args(input_filepath_list, input_format_list)
        args.extend(input_args)
        args.extend(self.effects)

        play(args)