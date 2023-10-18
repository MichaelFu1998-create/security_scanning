def eval(self, cmds, verbose=True, timeout=None, stream_handler=None,
             temp_dir=None, plot_dir=None, plot_name='plot', plot_format='svg',
             plot_width=None, plot_height=None, plot_res=None,
             nout=0, **kwargs):
        """
        Evaluate an Octave command or commands.

        Parameters
        ----------
        cmds : str or list
            Commands(s) to pass to Octave.
        verbose : bool, optional
             Log Octave output at INFO level.  If False, log at DEBUG level.
        stream_handler: callable, optional
            A function that is called for each line of output from the
            evaluation.
        timeout : float, optional
            Time to wait for response from Octave (per line).  If not given,
            the instance `timeout` is used.
        nout : int, optional.
            The desired number of returned values, defaults to 0.  If nout
            is 0, the `ans` will be returned as the return value.
        temp_dir: str, optional
            If specified, the session's MAT files will be created in the
            directory, otherwise a the instance `temp_dir` is used.
            a shared memory (tmpfs) path.
        plot_dir: str, optional
            If specificed, save the session's plot figures to the plot
            directory instead of displaying the plot window.
        plot_name : str, optional
            Saved plots will start with `plot_name` and
            end with "_%%.xxx' where %% is the plot number and
            xxx is the `plot_format`.
        plot_format: str, optional
            The format in which to save the plot (PNG by default).
        plot_width: int, optional
            The plot with in pixels.
        plot_height: int, optional
            The plot height in pixels.
        plot_res: int, optional
            The plot resolution in pixels per inch.
        **kwargs Deprectated kwargs.

        Examples
        --------
        >>> from oct2py import octave
        >>> octave.eval('disp("hello")') # doctest: +SKIP
        hello
        >>> x = octave.eval('round(quad(@sin, 0, pi/2));')
        >>> x
        1.0

        >>> a = octave.eval('disp("hello");1;')  # doctest: +SKIP
        hello
        >>> a = octave.eval('disp("hello");1;', verbose=False)
        >>> a
        1.0

        >>> from oct2py import octave
        >>> lines = []
        >>> octave.eval('for i = 1:3; disp(i);end', \
                        stream_handler=lines.append)
        >>> lines  # doctest: +SKIP
        [' 1', ' 2', ' 3']

        Returns
        -------
        out : object
            Octave "ans" variable, or None.

        Notes
        -----
        The deprecated `log` kwarg will temporarily set the `logger` level to
        `WARN`.  Using the `logger` settings directly is preferred.
        The deprecated `return_both` kwarg will still work, but the preferred
        method is to use the `stream_handler`.  If `stream_handler` is given,
        the `return_both` kwarg will be honored but will give an empty string
        as the reponse.

        Raises
        ------
        Oct2PyError
            If the command(s) fail.
        """
        if isinstance(cmds, (str, unicode)):
            cmds = [cmds]

        prev_temp_dir = self.temp_dir
        self.temp_dir = temp_dir or self.temp_dir
        prev_log_level = self.logger.level

        if kwargs.get('log') is False:
            self.logger.setLevel(logging.WARN)

        for name in ['log', 'return_both']:
            if name not in kwargs:
                continue
            msg = 'Using deprecated `%s` kwarg, see docs on `Oct2Py.eval()`'
            warnings.warn(msg % name, stacklevel=2)

        return_both = kwargs.pop('return_both', False)
        lines = []
        if return_both and not stream_handler:
            stream_handler = lines.append

        ans = None
        for cmd in cmds:
            resp = self.feval('evalin', 'base', cmd,
                              nout=nout, timeout=timeout,
                              stream_handler=stream_handler,
                              verbose=verbose, plot_dir=plot_dir,
                              plot_name=plot_name, plot_format=plot_format,
                              plot_width=plot_width, plot_height=plot_height,
                              plot_res=plot_res)
            if resp is not None:
                ans = resp

        self.temp_dir = prev_temp_dir
        self.logger.setLevel(prev_log_level)

        if return_both:
            return '\n'.join(lines), ans
        return ans