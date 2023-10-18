def interpolated(self):
        """B-spline function over the data grid(x,y,z).

        The :func:`interpolated` function allows one to obtain data
        values for any values of the coordinates::

           interpolated([x1,x2,...],[y1,y2,...],[z1,z2,...]) -> F[x1,y1,z1],F[x2,y2,z2],...

        The interpolation order is set in
        :attr:`Grid.interpolation_spline_order`.

        The interpolated function is computed once and is cached for better
        performance. Whenever :attr:`~Grid.interpolation_spline_order` is
        modified, :meth:`Grid.interpolated` is recomputed.

        The value for unknown data is set in :attr:`Grid.interpolation_cval`
        (TODO: also recompute when ``interpolation_cval`` value is changed.)

        Example
        -------
        Example usage for resampling::

           XX, YY, ZZ = numpy.mgrid[40:75:0.5, 96:150:0.5, 20:50:0.5]
           FF = interpolated(XX, YY, ZZ)

        Note
        ----
        Values are interpolated with a spline function. It is possible
        that the spline will generate values that would not normally
        appear in the data. For example, a density is non-negative but
        a cubic spline interpolation can generate negative values,
        especially at the boundary between 0 and high values.

        """
        if self.__interpolated is None:
            self.__interpolated = self._interpolationFunctionFactory()
        return self.__interpolated