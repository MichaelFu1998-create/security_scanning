def plot_coarsened(self, **kwargs):
        """Plot data like :meth:`XVG.plot` with the range of **all** data shown.

        Data are reduced to *maxpoints* (good results are obtained
        with low values such as 100) and the actual range of observed
        data is plotted as a translucent error band around the mean.

        Each column in *columns* (except the abscissa, i.e. the first
        column) is decimated (with :meth:`XVG.decimate`) and the range
        of data is plotted alongside the mean using
        :meth:`XVG.errorbar` (see for arguments). Additional
        arguments:

        :Kewords:
           *maxpoints*
                number of points (bins) to coarsen over
           *color*
                single color (used for all plots); sequence of colors
                (will be repeated as necessary); or a matplotlib
                colormap (e.g. "jet", see :mod:`matplotlib.cm`). The
                default is to use the :attr:`XVG.default_color_cycle`.
           *method*
                Method to coarsen the data. See :meth:`XVG.decimate`

        The *demean* keyword has no effect as it is required to be ``True``.

        .. SeeAlso:: :meth:`XVG.plot`, :meth:`XVG.errorbar` and :meth:`XVG.decimate`
        """
        ax = kwargs.pop('ax', None)
        columns = kwargs.pop('columns', Ellipsis)         # slice for everything
        if columns is Ellipsis or columns is None:
            columns = numpy.arange(self.array.shape[0])
        if len(columns) < 2:
            raise MissingDataError("plot_coarsened() assumes that there is at least one column "
                                   "of data for the abscissa and one or more for the ordinate.")

        color = kwargs.pop('color', self.default_color_cycle)
        try:
            cmap = matplotlib.cm.get_cmap(color)
            colors = cmap(matplotlib.colors.Normalize()(numpy.arange(len(columns[1:]), dtype=float)))
        except TypeError:
            colors = cycle(utilities.asiterable(color))

        if ax is None:
            ax = plt.gca()

        t = columns[0]
        kwargs['demean'] = True
        kwargs['ax'] = ax
        for column, color in zip(columns[1:], colors):
            kwargs['color'] = color
            self.errorbar(columns=[t, column, column], **kwargs)
        return ax