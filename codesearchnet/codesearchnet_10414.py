def decimate(self, method, a, maxpoints=10000, **kwargs):
        """Decimate data *a* to *maxpoints* using *method*.

        If *a* is a 1D array then it is promoted to a (2, N) array
        where the first column simply contains the index.

        If the array contains fewer than *maxpoints* points or if
        *maxpoints* is ``None`` then it is returned as it is. The
        default for *maxpoints* is 10000.

        Valid values for the reduction *method*:

          * "mean", uses :meth:`XVG.decimate_mean` to coarse grain by
            averaging the data in bins along the time axis

          * "circmean", uses :meth:`XVG.decimate_circmean` to coarse
            grain by calculating the circular mean of the data in bins
            along the time axis. Use additional keywords *low* and
            *high* to set the limits. Assumes that the data are in
            degrees.

          * "min" and "max* select the extremum in each bin

          * "rms", uses :meth:`XVG.decimate_rms` to coarse grain by
            computing the root mean square sum of the data in bins
            along the time axis (for averaging standard deviations and
            errors)

          * "percentile" with keyword *per*: :meth:`XVG.decimate_percentile`
            reduces data in each bin to the percentile *per*

          * "smooth", uses :meth:`XVG.decimate_smooth` to subsample
            from a smoothed function (generated with a running average
            of the coarse graining step size derived from the original
            number of data points and *maxpoints*)

        :Returns: numpy array ``(M', N')`` from a ``(M', N)`` array
                  with ``M' == M`` (except when ``M == 1``, see above)
                  and ``N' <= N`` (``N'`` is *maxpoints*).
        """
        methods = {'mean': self.decimate_mean,
                   'min': self.decimate_min,
                   'max': self.decimate_max,
                   'smooth': self.decimate_smooth,
                   'rms': self.decimate_rms,
                   'percentile': self.decimate_percentile,
                   'error': self.decimate_error,  # undocumented, not working well
                   'circmean': self.decimate_circmean,
                   }
        if len(a.shape) == 1:
            # add first column as index
            # (probably should do this in class/init anyway...)
            X = numpy.arange(len(a))
            a = numpy.vstack([X, a])
        ny = a.shape[-1]   # assume 1D or 2D array with last dimension varying fastest
        if maxpoints is None or ny <= maxpoints:
            return a
        return methods[method](a, maxpoints, **kwargs)