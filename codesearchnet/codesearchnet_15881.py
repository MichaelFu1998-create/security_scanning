def feval(self, func_path, *func_args, **kwargs):
        """Run a function in Octave and return the result.

        Parameters
        ----------
        func_path: str
            Name of function to run or a path to an m-file.
        func_args: object, optional
            Args to send to the function.
        nout: int, optional
            Desired number of return arguments, defaults to 1.
        store_as: str, optional
            If given, saves the result to the given Octave variable name
            instead of returning it.
        verbose : bool, optional
            Log Octave output at INFO level.  If False, log at DEBUG level.
        stream_handler: callable, optional
            A function that is called for each line of output from the
            evaluation.
        timeout: float, optional
            The timeout in seconds for the call.
        plot_dir: str, optional
            If specificed, save the session's plot figures to the plot
            directory instead of displaying the plot window.
        plot_name : str, optional
            Saved plots will start with `plot_name` and
            end with "_%%.xxx' where %% is the plot number and
            xxx is the `plot_format`.
        plot_format: str, optional
            The format in which to save the plot.
        plot_width: int, optional
            The plot with in pixels.
        plot_height: int, optional
            The plot height in pixels.

        Notes
        -----
        The function arguments passed follow Octave calling convention, not
        Python. That is, all values must be passed as a comma separated list,
        not using `x=foo` assignment.

        Examples
        --------
        >>> from oct2py import octave
        >>> cell = octave.feval('cell', 10, 10, 10)
        >>> cell.shape
        (10, 10, 10)

        >>> from oct2py import octave
        >>> x = octave.feval('linspace', 0, octave.pi() / 2)
        >>> x.shape
        (1, 100)

        >>> from oct2py import octave
        >>> x = octave.feval('svd', octave.hilb(3))
        >>> x
        array([[ 1.40831893],
               [ 0.12232707],
               [ 0.00268734]])
        >>> # specify three return values
        >>> (u, v, d) = octave.feval('svd', octave.hilb(3), nout=3)
        >>> u.shape
        (3, 3)

        Returns
        -------
        The Python value(s) returned by the Octave function call.
        """
        if not self._engine:
            raise Oct2PyError('Session is not open')

        nout = kwargs.get('nout', None)
        if nout is None:
            nout = 1

        plot_dir = kwargs.get('plot_dir')
        settings = dict(backend='inline' if plot_dir else self.backend,
                        format=kwargs.get('plot_format'),
                        name=kwargs.get('plot_name'),
                        width=kwargs.get('plot_width'),
                        height=kwargs.get('plot_height'),
                        resolution=kwargs.get('plot_res'))
        self._engine.plot_settings = settings

        dname = osp.dirname(func_path)
        fname = osp.basename(func_path)
        func_name, ext = osp.splitext(fname)
        if ext and not ext == '.m':
            raise TypeError('Need to give path to .m file')

        if func_name == 'clear':
            raise Oct2PyError('Cannot use `clear` command directly, use' +
                              ' eval("clear(var1, var2)")')

        stream_handler = kwargs.get('stream_handler')
        verbose = kwargs.get('verbose', True)
        store_as = kwargs.get('store_as', '')
        timeout = kwargs.get('timeout', self.timeout)
        if not stream_handler:
            stream_handler = self.logger.info if verbose else self.logger.debug

        return self._feval(func_name, func_args, dname=dname, nout=nout,
                          timeout=timeout, stream_handler=stream_handler,
                          store_as=store_as, plot_dir=plot_dir)