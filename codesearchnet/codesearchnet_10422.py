def decimate_smooth(self, a, maxpoints, window="flat"):
        """Return smoothed data *a* decimated on approximately *maxpoints* points.

        1. Produces a smoothed graph using the smoothing window *window*;
           "flat" is a running average.
        2. select points at a step size approximatelt producing maxpoints

        If *a* contains <= *maxpoints* then *a* is simply returned;
        otherwise a new array of the same dimensions but with a
        reduced number of points (close to *maxpoints*) is returned.

        .. Note::

           Assumes that the first column is time (which will *never*
           be smoothed/averaged), except when the input array *a* is
           1D and therefore to be assumed to be data at equidistance
           timepoints.

        TODO:
        - Allow treating the 1st column as data
        """
        ny = a.shape[-1]   # assume 1D or 2D array with last dimension varying fastest
        # reduce size by averaging oover stepsize steps and then just
        # picking every stepsize data points.  (primitive --- can
        # leave out bits at the end or end up with almost twice of
        # maxpoints)
        stepsize = int(ny / maxpoints)
        if stepsize % 2 == 0:
            stepsize += 1  # must be odd for the running average/smoothing window
        out = numpy.empty_like(a)

        # smoothed
        out[0,:] = a[0]
        for i in range(1, a.shape[0]):
            # process columns because smooth() only handles 1D arrays :-p
            out[i,:] = numkit.timeseries.smooth(a[i], stepsize, window=window)

        if maxpoints == self.maxpoints_default:  # only warn if user did not set maxpoints
            warnings.warn("Plot had %d datapoints > maxpoints = %d; decimated to %d regularly "
                          "spaced points with smoothing (%r) over %d steps."
                          % (ny, maxpoints, ny/stepsize, window, stepsize),
                          category=AutoCorrectionWarning)
        return out[..., ::stepsize]