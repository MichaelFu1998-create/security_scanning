def build(self, input_filepath_list, output_filepath, combine_type,
              input_volumes=None):
        '''Builds the output_file by executing the current set of commands.

        Parameters
        ----------
        input_filepath_list : list of str
            List of paths to input audio files.
        output_filepath : str
            Path to desired output file. If a file already exists at the given
            path, the file will be overwritten.
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
        file_info.validate_input_file_list(input_filepath_list)
        file_info.validate_output_file(output_filepath)
        _validate_combine_type(combine_type)
        _validate_volumes(input_volumes)

        input_format_list = _build_input_format_list(
            input_filepath_list, input_volumes, self.input_format
        )

        try:
            _validate_file_formats(input_filepath_list, combine_type)
        except SoxiError:
            logger.warning("unable to validate file formats.")

        args = []
        args.extend(self.globals)
        args.extend(['--combine', combine_type])

        input_args = _build_input_args(input_filepath_list, input_format_list)
        args.extend(input_args)

        args.extend(self.output_format)
        args.append(output_filepath)
        args.extend(self.effects)

        status, out, err = sox(args)

        if status != 0:
            raise SoxError(
                "Stdout: {}\nStderr: {}".format(out, err)
            )
        else:
            logger.info(
                "Created %s with combiner %s and  effects: %s",
                output_filepath,
                combine_type,
                " ".join(self.effects_log)
            )
            if out is not None:
                logger.info("[SoX] {}".format(out))
            return True