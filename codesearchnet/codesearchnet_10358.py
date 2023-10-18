def Popen(self, *args, **kwargs):
        """Returns a special Popen instance (:class:`PopenWithInput`).

        The instance has its input pre-set so that calls to
        :meth:`~PopenWithInput.communicate` will not need to supply
        input. This is necessary if one wants to chain the output from
        one command to an input from another.

        :TODO:
          Write example.
        """
        stderr = kwargs.pop('stderr', None)     # default: print to stderr (if STDOUT then merge)
        if stderr is False:                     # False: capture it
            stderr = PIPE
        elif stderr is True:
            stderr = None                       # use stderr

        stdout = kwargs.pop('stdout', None)     # either set to PIPE for capturing output
        if stdout is False:                     # ... or to False
            stdout = PIPE
        elif stdout is True:
            stdout = None                       # for consistency, make True write to screen

        stdin = kwargs.pop('stdin', None)
        input = kwargs.pop('input', None)

        use_shell = kwargs.pop('use_shell', False)
        if input:
            stdin = PIPE
            if isinstance(input, six.string_types) and not input.endswith('\n'):
                # make sure that input is a simple string with \n line endings
                input = six.text_type(input) + '\n'
            else:
                try:
                    # make sure that input is a simple string with \n line endings
                    input = '\n'.join(map(six.text_type, input)) + '\n'
                except TypeError:
                    # so maybe we are a file or something ... and hope for the best
                    pass

        cmd = self._commandline(*args, **kwargs)   # lots of magic happening here
                                                   # (cannot move out of method because filtering of stdin etc)
        try:
            p = PopenWithInput(cmd, stdin=stdin, stderr=stderr, stdout=stdout,
                               universal_newlines=True, input=input, shell=use_shell)
        except OSError as err:
            logger.error(" ".join(cmd))            # log command line
            if err.errno == errno.ENOENT:
                errmsg = "Failed to find Gromacs command {0!r}, maybe its not on PATH or GMXRC must be sourced?".format(self.command_name)
                logger.fatal(errmsg)
                raise OSError(errmsg)
            else:
                logger.exception("Setting up Gromacs command {0!r} raised an exception.".format(self.command_name))
                raise
        logger.debug(p.command_string)
        return p