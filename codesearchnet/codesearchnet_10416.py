def decimate_circmean(self, a, maxpoints, **kwargs):
        """Return data *a* circmean-decimated on *maxpoints*.

        Histograms each column into *maxpoints* bins and calculates
        the weighted circular mean in each bin as the decimated data,
        using
        :func:`numkit.timeseries.circmean_histogrammed_function`. The
        coarse grained time in the first column contains the centers
        of the histogram time.

        If *a* contains <= *maxpoints* then *a* is simply returned;
        otherwise a new array of the same dimensions but with a
        reduced number of  *maxpoints* points is returned.

        Keywords *low* and *high* can be used to set the
        boundaries. By default they are [-pi, +pi].

        This method returns a **masked** array where jumps are flagged
        by an insertion of a masked point.

        .. Note::

           Assumes that the first column is time and that the data are
           in **degrees**.

        .. Warning::

           Breaking of arrays only works properly with a two-column
           array because breaks are only inserted in the x-column
           (a[0]) where y1 = a[1] has a break.

        """
        a_rad = numpy.vstack((a[0], numpy.deg2rad(a[1:])))
        b = self._decimate(numkit.timeseries.circmean_histogrammed_function, a_rad, maxpoints, **kwargs)
        y_ma, x_ma = break_array(b[1], threshold=numpy.pi, other=b[0])
        v = [y_ma]
        for y in b[2:]:
            v.append(break_array(y, threshold=numpy.pi)[0])
            if v[-1].shape != v[0].shape:
                raise ValueError("y dimensions have different breaks: you MUST deal with them separately")
        return numpy.vstack((x_ma, numpy.rad2deg(v)))