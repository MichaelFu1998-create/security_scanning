def _interpolationFunctionFactory(self, spline_order=None, cval=None):
        """Returns a function F(x,y,z) that interpolates any values on the grid.

        _interpolationFunctionFactory(self,spline_order=3,cval=None) --> F

        *cval* is set to :meth:`Grid.grid.min`. *cval* cannot be chosen too
        large or too small or NaN because otherwise the spline interpolation
        breaks down near that region and produces wild oscillations.

        .. Note:: Only correct for equally spaced values (i.e. regular edges with
                  constant delta).
        .. SeeAlso:: http://www.scipy.org/Cookbook/Interpolation
        """
        # for scipy >=0.9: should use scipy.interpolate.griddata
        # http://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.griddata.html#scipy.interpolate.griddata
        # (does it work for nD?)
        import scipy.ndimage

        if spline_order is None:
            # must be compatible with whatever :func:`scipy.ndimage.spline_filter` takes.
            spline_order = self.interpolation_spline_order
        if cval is None:
            cval = self.interpolation_cval

        data = self.grid
        if cval is None:
            cval = data.min()
        try:
            # masked arrays, fill with min: should keep spline happy
            _data = data.filled(cval)
        except AttributeError:
            _data = data

        coeffs = scipy.ndimage.spline_filter(_data, order=spline_order)
        x0 = self.origin
        dx = self.delta

        def _transform(cnew, c0, dc):
            return (numpy.atleast_1d(cnew) - c0) / dc

        def interpolatedF(*coordinates):
            """B-spline function over the data grid(x,y,z).

            interpolatedF([x1,x2,...],[y1,y2,...],[z1,z2,...]) -> F[x1,y1,z1],F[x2,y2,z2],...

            Example usage for resampling::
              >>> XX,YY,ZZ = numpy.mgrid[40:75:0.5, 96:150:0.5, 20:50:0.5]
              >>> FF = _interpolationFunction(XX,YY,ZZ)
            """
            _coordinates = numpy.array(
                [_transform(coordinates[i], x0[i], dx[i]) for i in range(len(
                    coordinates))])
            return scipy.ndimage.map_coordinates(coeffs,
                                                 _coordinates,
                                                 prefilter=False,
                                                 mode='nearest',
                                                 cval=cval)
        # mode='wrap' would be ideal but is broken: https://github.com/scipy/scipy/issues/1323
        return interpolatedF