def set_globals(self, dither=False, guard=False, multithread=False,
                    replay_gain=False, verbosity=2):
        '''Sets SoX's global arguments.
        Overwrites any previously set global arguments.
        If this function is not explicity called, globals are set to this
        function's defaults.

        Parameters
        ----------
        dither : bool, default=False
            If True, dithering is applied for low files with low bit rates.
        guard : bool, default=False
            If True, invokes the gain effect to guard against clipping.
        multithread : bool, default=False
            If True, each channel is processed in parallel.
        replay_gain : bool, default=False
            If True, applies replay-gain adjustment to input-files.
        verbosity : int, default=2
            SoX's verbosity level. One of:
                * 0 : No messages are shown at all
                * 1 : Only error messages are shown. These are generated if SoX
                    cannot complete the requested commands.
                * 2 : Warning messages are also shown. These are generated if
                    SoX can complete the requested commands, but not exactly
                    according to the requested command parameters, or if
                    clipping occurs.
                * 3 : Descriptions of SoX’s processing phases are also shown.
                    Useful for seeing exactly how SoX is processing your audio.
                * 4, >4 : Messages to help with debugging SoX are also shown.

        '''
        if not isinstance(dither, bool):
            raise ValueError('dither must be a boolean.')

        if not isinstance(guard, bool):
            raise ValueError('guard must be a boolean.')

        if not isinstance(multithread, bool):
            raise ValueError('multithread must be a boolean.')

        if not isinstance(replay_gain, bool):
            raise ValueError('replay_gain must be a boolean.')

        if verbosity not in VERBOSITY_VALS:
            raise ValueError(
                'Invalid value for VERBOSITY. Must be one {}'.format(
                    VERBOSITY_VALS)
            )

        global_args = []

        if not dither:
            global_args.append('-D')

        if guard:
            global_args.append('-G')

        if multithread:
            global_args.append('--multi-threaded')

        if replay_gain:
            global_args.append('--replay-gain')
            global_args.append('track')

        global_args.append('-V{}'.format(verbosity))

        self.globals = global_args
        return self