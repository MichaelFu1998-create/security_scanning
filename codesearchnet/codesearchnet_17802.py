def from_uniform(
            cls, z, origin=(0, 0), step=(1, 1), formatter=numpy_formatter):
        """Construct a contour generator from a uniform grid.

        NOTE
        ----
        The default `origin` and `step` values is equivalent to calling
        :meth:`matplotlib.axes.Axes.contour` with only the `z` argument.

        Parameters
        ----------
        z : array_like
            The 2-dimensional uniform grid of data to compute contours for.
            Masked arrays are supported.
        origin : (number.Number, number.Number)
            The (x, y) coordinate of data point `z[0,0]`.
        step :  (number.Number, number.Number)
            The (x, y) distance between data points in `z`.
        formatter : callable
            A conversion function to convert from the internal `Matplotlib`_
            contour format to an external format.  See :ref:`formatters` for
            more information.

        Returns
        -------
        : :class:`QuadContourGenerator`
            Initialized contour generator.

        """
        z = np.ma.asarray(z, dtype=np.float64)
        # Check arguments.
        if z.ndim != 2:
            raise TypeError(
                "'z' must be a 2D array but it a {:d}D array".format(z.ndim))
        if len(origin) != 2:
            raise TypeError(
                "'origin' must be of length 2 but has length {:d}".format(
                    len(origin)))
        if len(step) != 2:
            raise TypeError(
                "'step' must be of length 2 but has length {:d}".format(
                    len(step)))
        if any(s == 0 for s in step):
            raise ValueError(
                "'step' must have non-zero values but is {:s}".format(
                    str(step)))
        # Convert to curvilinear format and call constructor.
        y, x = np.mgrid[
            origin[0]:(origin[0]+step[0]*z.shape[0]):step[0],
            origin[1]:(origin[1]+step[1]*z.shape[1]):step[1]]
        return cls(x, y, z, formatter)