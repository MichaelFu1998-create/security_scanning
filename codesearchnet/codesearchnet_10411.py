def plot(self, **kwargs):
        """Plot xvg file data.

        The first column of the data is always taken as the abscissa
        X. Additional columns are plotted as ordinates Y1, Y2, ...

        In the special case that there is only a single column then this column
        is plotted against the index, i.e. (N, Y).

        :Keywords:
          *columns* : list
               Select the columns of the data to be plotted; the list
               is used as a numpy.array extended slice. The default is
               to use all columns. Columns are selected *after* a transform.
          *transform* : function
               function ``transform(array) -> array`` which transforms
               the original array; must return a 2D numpy array of
               shape [X, Y1, Y2, ...] where X, Y1, ... are column
               vectors.  By default the transformation is the
               identity [``lambda x: x``].
          *maxpoints* : int
               limit the total number of data points; matplotlib has issues processing
               png files with >100,000 points and pdfs take forever to display. Set to
               ``None`` if really all data should be displayed. At the moment we simply
               decimate the data at regular intervals. [10000]
          *method*
               method to decimate the data to *maxpoints*, see :meth:`XVG.decimate`
               for details
          *color*
               single color (used for all plots); sequence of colors
               (will be repeated as necessary); or a matplotlib
               colormap (e.g. "jet", see :mod:`matplotlib.cm`). The
               default is to use the :attr:`XVG.default_color_cycle`.
          *ax*
               plot into given axes or create new one if ``None`` [``None``]
          *kwargs*
               All other keyword arguments are passed on to :func:`matplotlib.pyplot.plot`.

        :Returns:
          *ax*
               axes instance
        """
        columns = kwargs.pop('columns', Ellipsis)         # slice for everything
        maxpoints = kwargs.pop('maxpoints', self.maxpoints_default)
        transform = kwargs.pop('transform', lambda x: x)  # default is identity transformation
        method = kwargs.pop('method', "mean")
        ax = kwargs.pop('ax', None)

        if columns is Ellipsis or columns is None:
            columns = numpy.arange(self.array.shape[0])
        if len(columns) == 0:
            raise MissingDataError("plot() needs at least one column of data")

        if len(self.array.shape) == 1 or self.array.shape[0] == 1:
            # special case: plot against index; plot would do this automatically but
            # we'll just produce our own xdata and pretend that this was X all along
            a = numpy.ravel(self.array)
            X = numpy.arange(len(a))
            a = numpy.vstack((X, a))
            columns = [0] + [c+1 for c in columns]
        else:
            a = self.array

        color = kwargs.pop('color', self.default_color_cycle)
        try:
            cmap = matplotlib.cm.get_cmap(color)
            colors = cmap(matplotlib.colors.Normalize()(numpy.arange(len(columns[1:]), dtype=float)))
        except TypeError:
            colors = cycle(utilities.asiterable(color))

        if ax is None:
            ax = plt.gca()

        # (decimate/smooth o slice o transform)(array)
        a = self.decimate(method, numpy.asarray(transform(a))[columns], maxpoints=maxpoints)

        # now deal with infs, nans etc AFTER all transformations (needed for plotting across inf/nan)
        ma = numpy.ma.MaskedArray(a, mask=numpy.logical_not(numpy.isfinite(a)))

        # finally plot (each column separately to catch empty sets)
        for column, color in zip(range(1,len(columns)), colors):
            if len(ma[column]) == 0:
                warnings.warn("No data to plot for column {column:d}".format(**vars()), category=MissingDataWarning)
            kwargs['color'] = color
            ax.plot(ma[0], ma[column], **kwargs)   # plot all other columns in parallel
        return ax