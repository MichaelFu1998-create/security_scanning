def _update(self):
        """compute/update all derived data

        Can be called without harm and is idem-potent.

        Updates these attributes and methods:
           :attr:`origin`
              the center of the cell with index 0,0,0
           :attr:`midpoints`
              centre coordinate of each grid cell
           :meth:`interpolated`
              spline interpolation function that can generated a value for
              coordinate
        """
        self.delta = numpy.array(list(
            map(lambda e: (e[-1] - e[0]) / (len(e) - 1), self.edges)))
        self.midpoints = self._midpoints(self.edges)
        self.origin = numpy.array(list(map(lambda m: m[0], self.midpoints)))
        if self.__interpolated is not None:
            # only update if we are using it
            self.__interpolated = self._interpolationFunctionFactory()