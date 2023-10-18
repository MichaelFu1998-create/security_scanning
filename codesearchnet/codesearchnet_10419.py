def decimate_rms(self, a, maxpoints, **kwargs):
        """Return data *a* rms-decimated on *maxpoints*.

        Histograms each column into *maxpoints* bins and calculates
        the root mean square sum in each bin as the decimated data,
        using :func:`numkit.timeseries.rms_histogrammed_function`. The coarse
        grained time in the first column contains the centers of the
        histogram time.

        If *a* contains <= *maxpoints* then *a* is simply returned;
        otherwise a new array of the same dimensions but with a
        reduced number of  *maxpoints* points is returned.

        .. Note::

           Assumes that the first column is time.

        """
        return self._decimate(numkit.timeseries.rms_histogrammed_function, a, maxpoints, **kwargs)