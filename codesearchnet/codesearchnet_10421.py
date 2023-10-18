def decimate_error(self, a, maxpoints, **kwargs):
        """Return data *a* error-decimated on *maxpoints*.

        Histograms each column into *maxpoints* bins and calculates an
        error estimate in each bin as the decimated data, using
        :func:`numkit.timeseries.error_histogrammed_function`. The
        coarse grained time in the first column contains the centers
        of the histogram time.

        If *a* contains <= *maxpoints* then *a* is simply returned;
        otherwise a new array of the same dimensions but with a
        reduced number of  *maxpoints* points is returned.

        .. SeeAlso:: :func:`numkit.timeseries.tcorrel`

        .. Note::

           Assumes that the first column is time.

           Does not work very well because often there are too few
           datapoints to compute a good autocorrelation function.

        """
        warnings.warn("Using undocumented decimate_error() is highly EXPERIMENTAL",
                      category=gromacs.exceptions.LowAccuracyWarning)
        return self._decimate(numkit.timeseries.error_histogrammed_function, a,
                              maxpoints, **kwargs)