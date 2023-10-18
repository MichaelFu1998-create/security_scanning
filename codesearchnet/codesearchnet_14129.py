def _get_length(self, segmented=False, precision=10):
        """ Returns the length of the path.
            Calculates the length of each spline in the path, using n as a number of points to measure.
            When segmented is True, returns a list containing the individual length of each spline
            as values between 0.0 and 1.0, defining the relative length of each spline
            in relation to the total path length.
        """
        # Originally from nodebox-gl
        if not segmented:
            return sum(self._segment_lengths(n=precision), 0.0)
        else:
            return self._segment_lengths(relative=True, n=precision)