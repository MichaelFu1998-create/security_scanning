def errorbar(self, **kwargs):
        """errorbar plot for a single time series with errors.

        Set *columns* keyword to select [x, y, dy] or [x, y, dx, dy],
        e.g. ``columns=[0,1,2]``. See :meth:`XVG.plot` for
        details. Only a single timeseries can be plotted and the user
        needs to select the appropriate columns with the *columns*
        keyword.

        By default, the data are decimated (see :meth:`XVG.plot`) for
        the default of *maxpoints* = 10000 by averaging data in
        *maxpoints* bins.

        x,y,dx,dy data can plotted with error bars in the x- and
        y-dimension (use *filled* = ``False``).

        For x,y,dy use *filled* = ``True`` to fill the region between
        y±dy. *fill_alpha* determines the transparency of the fill
        color. *filled* = ``False`` will draw lines for the error
        bars. Additional keywords are passed to
        :func:`pylab.errorbar`.

        By default, the errors are decimated by plotting the 5% and
        95% percentile of the data in each bin. The percentile can be
        changed with the *percentile* keyword; e.g. *percentile* = 1
        will plot the 1% and 99% perentile (as will *percentile* =
        99).

        The *error_method* keyword can be used to compute errors as
        the root mean square sum (*error_method* = "rms") across each
        bin instead of percentiles ("percentile"). The value of the
        keyword *demean* is applied to the decimation of error data
        alone.

        .. SeeAlso::

           :meth:`XVG.plot` lists keywords common to both methods.
        """
        ax = kwargs.pop('ax', None)
        color = kwargs.pop('color', 'black')
        filled = kwargs.pop('filled', True)
        fill_alpha = kwargs.pop('fill_alpha', 0.2)

        kwargs.setdefault('capsize', 0)
        kwargs.setdefault('elinewidth', 1)
        kwargs.setdefault('ecolor', color)
        kwargs.setdefault('alpha', 0.3)
        kwargs.setdefault('fmt', None)

        columns = kwargs.pop('columns', Ellipsis)         # slice for everything
        maxpoints = kwargs.pop('maxpoints', self.maxpoints_default)
        transform = kwargs.pop('transform', lambda x: x)  # default is identity transformation
        method = kwargs.pop('method', "mean")
        if method != "mean":
            raise NotImplementedError("For errors only method == 'mean' is supported.")
        error_method = kwargs.pop('error_method', "percentile")  # can also use 'rms' and 'error'
        percentile = numpy.abs(kwargs.pop('percentile', 95.))
        demean = kwargs.pop('demean', False)

        # order: (decimate/smooth o slice o transform)(array)
        try:
            data = numpy.asarray(transform(self.array))[columns]
        except IndexError:
            raise MissingDataError("columns {0!r} are not suitable to index the transformed array, possibly not eneough data".format(columns))
        if data.shape[-1] == 0:
            raise MissingDataError("There is no data to be plotted.")
        a = numpy.zeros((data.shape[0], maxpoints), dtype=numpy.float64)
        a[0:2] = self.decimate("mean", data[0:2], maxpoints=maxpoints)
        error_data = numpy.vstack((data[0], data[2:]))
        if error_method == "percentile":
            if percentile > 50:
                upper_per = percentile
                lower_per = 100 - percentile
            else:
                upper_per = 100 - percentile
                lower_per = percentile
            # demean generally does not make sense with the percentiles (but for analysing
            # the regularised data itself we use this as a flag --- see below!)
            upper = a[2:] = self.decimate("percentile", error_data, maxpoints=maxpoints,
                                          per=upper_per, demean=False)[1:]
            lower = self.decimate("percentile", error_data, maxpoints=maxpoints,
                                  per=lower_per, demean=False)[1:]
        else:
            a[2:] = self.decimate(error_method, error_data, maxpoints=maxpoints, demean=demean)[1:]
            lower = None

        # now deal with infs, nans etc AFTER all transformations (needed for plotting across inf/nan)
        ma = numpy.ma.MaskedArray(a, mask=numpy.logical_not(numpy.isfinite(a)))
        if lower is not None:
            mlower = numpy.ma.MaskedArray(lower, mask=numpy.logical_not(numpy.isfinite(lower)))

        # finally plot
        X = ma[0]          # abscissa set separately
        Y = ma[1]
        try:
            kwargs['yerr'] = ma[3]
            kwargs['xerr'] = ma[2]
        except IndexError:
            try:
                kwargs['yerr'] = ma[2]
            except IndexError:
                raise TypeError("Either too few columns selected or data does not have a error column")

        if ax is None:
            ax = plt.gca()

        if filled:
            # can only plot dy
            if error_method == "percentile":
                if demean:
                    # signal that we are looking at percentiles of an observable and not error
                    y1 = mlower[-1]
                    y2 = kwargs['yerr']
                else:
                    # percentiles of real errors (>0)
                    y1 = Y - mlower[-1]
                    y2 = Y + kwargs['yerr']
            else:
                y1 = Y - kwargs['yerr']
                y2 = Y + kwargs['yerr']
            ax.fill_between(X, y1, y2, color=color, alpha=fill_alpha)
        else:
            if error_method == "percentile":
                # errorbars extend to different lengths;
                if demean:
                    kwargs['yerr'] = numpy.vstack((mlower[-1], kwargs['yerr']))
                else:
                    kwargs['yerr'] = numpy.vstack((Y - mlower[-1], Y + kwargs['yerr']))
                try:
                    # xerr only makes sense when the data is a real
                    # error so we don't even bother with demean=?
                    kwargs['xerr'] = numpy.vstack((X - mlower[0], X + kwargs['xerr']))
                except (KeyError, IndexError):
                    pass
            ax.errorbar(X, Y, **kwargs)

        # clean up args for plot
        for kw in "yerr", "xerr", "capsize", "ecolor", "elinewidth", "fmt":
            kwargs.pop(kw, None)
        kwargs['alpha'] = 1.0

        ax.plot(X, Y, color=color, **kwargs)

        return ax