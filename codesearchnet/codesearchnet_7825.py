def build(self, input_filepath, output_filepath, extra_args=None,
              return_output=False):
        '''Builds the output_file by executing the current set of commands.

        Parameters
        ----------
        input_filepath : str
            Path to input audio file.
        output_filepath : str or None
            Path to desired output file. If a file already exists at the given
            path, the file will be overwritten.
            If None, no file will be created.
        extra_args : list or None, default=None
            If a list is given, these additional arguments are passed to SoX
            at the end of the list of effects.
            Don't use this argument unless you know exactly what you're doing!
        return_output : bool, default=False
            If True, returns the status and information sent to stderr and
            stdout as a tuple (status, stdout, stderr).
            Otherwise returns True on success.

        '''
        file_info.validate_input_file(input_filepath)

        if output_filepath is not None:
            file_info.validate_output_file(output_filepath)
        else:
            output_filepath = '-n'

        if input_filepath == output_filepath:
            raise ValueError(
                "input_filepath must be different from output_filepath."
            )

        args = []
        args.extend(self.globals)
        args.extend(self.input_format)
        args.append(input_filepath)
        args.extend(self.output_format)
        args.append(output_filepath)
        args.extend(self.effects)

        if extra_args is not None:
            if not isinstance(extra_args, list):
                raise ValueError("extra_args must be a list.")
            args.extend(extra_args)

        status, out, err = sox(args)

        if status != 0:
            raise SoxError(
                "Stdout: {}\nStderr: {}".format(out, err)
            )
        else:
            logger.info(
                "Created %s with effects: %s",
                output_filepath,
                " ".join(self.effects_log)
            )
            if out is not None:
                logger.info("[SoX] {}".format(out))

            if return_output:
                return status, out, err
            else:
                return True