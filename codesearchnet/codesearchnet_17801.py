def from_rectilinear(cls, x, y, z, formatter=numpy_formatter):
        """Construct a contour generator from a rectilinear grid.

        Parameters
        ----------
        x : array_like
            x coordinates of each column of `z`.  Must be the same length as
            the number of columns in `z`.  (len(x) == z.shape[1])
        y : array_like
            y coordinates of each row of `z`.  Must be the same length as the
            number of columns in `z`.  (len(y) == z.shape[0])
        z : array_like
            The 2-dimensional rectilinear grid of data to compute contours for.
            Masked arrays are supported.
        formatter : callable
            A conversion function to convert from the internal `Matplotlib`_
            contour format to an external format.  See :ref:`formatters` for
            more information.

        Returns
        -------
        : :class:`QuadContourGenerator`
            Initialized contour generator.

        """
        x = np.asarray(x, dtype=np.float64)
        y = np.asarray(y, dtype=np.float64)
        z = np.ma.asarray(z, dtype=np.float64)
        # Check arguments.
        if x.ndim != 1:
            raise TypeError(
                "'x' must be a 1D array but is a {:d}D array".format(x.ndim))
        if y.ndim != 1:
            raise TypeError(
                "'y' must be a 1D array but is a {:d}D array".format(y.ndim))
        if z.ndim != 2:
            raise TypeError(
                "'z' must be a 2D array but it a {:d}D array".format(z.ndim))
        if x.size != z.shape[1]:
            raise TypeError(
                ("the length of 'x' must be equal to the number of columns in "
                 "'z' but the length of 'x' is {:d} and 'z' has {:d} "
                 "columns").format(x.size, z.shape[1]))
        if y.size != z.shape[0]:
            raise TypeError(
                ("the length of 'y' must be equal to the number of rows in "
                 "'z' but the length of 'y' is {:d} and 'z' has {:d} "
                 "rows").format(y.size, z.shape[0]))
        # Convert to curvilinear format and call constructor.
        y, x = np.meshgrid(y, x, indexing='ij')
        return cls(x, y, z, formatter)