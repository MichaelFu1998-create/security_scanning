def resample(self, edges):
        """Resample data to a new grid with edges *edges*.

        This method creates a new grid with the data from the current
        grid resampled to a regular grid specified by *edges*.  The
        order of the interpolation is set by
        :attr:`Grid.interpolation_spline_order`: change the value
        *before* calling :meth:`resample`.

        Parameters
        ----------
        edges : tuple of arrays or Grid
             edges of the new grid or a :class:`Grid` instance that
             provides :attr:`Grid.edges`

        Returns
        -------
        Grid
             a new :class:`Grid` with the data interpolated over the
             new grid cells


        Examples
        --------

        Providing *edges* (a tuple of three arrays, indicating the
        boundaries of each grid cell)::

          g = grid.resample(edges)

        As a convenience, one can also supply another :class:`Grid` as
        the argument for this method ::

          g = grid.resample(othergrid)

        and the edges are taken from :attr:`Grid.edges`.

        """
        try:
            edges = edges.edges  # can also supply another Grid
        except AttributeError:
            pass
        midpoints = self._midpoints(edges)
        coordinates = ndmeshgrid(*midpoints)
        # feed a meshgrid to generate all points
        newgrid = self.interpolated(*coordinates)
        return self.__class__(newgrid, edges)