def decimate_percentile(self, a, maxpoints, **kwargs):
        """Return data *a* percentile-decimated on *maxpoints*.

        Histograms each column into *maxpoints* bins and calculates
        the percentile *per* in each bin as the decimated data, using
        :func:`numkit.timeseries.percentile_histogrammed_function`. The
        coarse grained time in the first column contains the centers
        of the histogram time.

        If *a* contains <= *maxpoints* then *a* is simply returned;
        otherwise a new array of the same dimensions but with a
        reduced number of  *maxpoints* points is returned.

        .. Note::

           Assumes that the first column is time.

        :Keywords:

        *per*
            percentile as a percentage, e.g. 75 is the value that splits
            the data into the lower 75% and upper 25%; 50 is the median [50.0]

        .. SeeAlso:: :func:`numkit.timeseries.regularized_function` with :func:`scipy.stats.scoreatpercentile`
        """
        return self._decimate(numkit.timeseries.percentile_histogrammed_function, a, maxpoints, **kwargs)