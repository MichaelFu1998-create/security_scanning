def lightcurve_moments(ftimes, fmags, ferrs):
    '''This calculates the weighted mean, stdev, median, MAD, percentiles, skew,
    kurtosis, fraction of LC beyond 1-stdev, and IQR.

    Parameters
    ----------

    ftimes,fmags,ferrs : np.array
        The input mag/flux time-series with all non-finite elements removed.

    Returns
    -------

    dict
        A dict with all of the light curve moments calculated.

    '''

    ndet = len(fmags)

    if ndet > 9:

        # now calculate the various things we need
        series_median = npmedian(fmags)
        series_wmean = (
            npsum(fmags*(1.0/(ferrs*ferrs)))/npsum(1.0/(ferrs*ferrs))
        )
        series_mad = npmedian(npabs(fmags - series_median))
        series_stdev = 1.483*series_mad
        series_skew = spskew(fmags)
        series_kurtosis = spkurtosis(fmags)

        # get the beyond1std fraction
        series_above1std = len(fmags[fmags > (series_median + series_stdev)])
        series_below1std = len(fmags[fmags < (series_median - series_stdev)])

        # this is the fraction beyond 1 stdev
        series_beyond1std = (series_above1std + series_below1std)/float(ndet)

        # get the magnitude percentiles
        series_mag_percentiles = nppercentile(
            fmags,
            [5.0,10,17.5,25,32.5,40,60,67.5,75,82.5,90,95]
        )

        return {
            'median':series_median,
            'wmean':series_wmean,
            'mad':series_mad,
            'stdev':series_stdev,
            'skew':series_skew,
            'kurtosis':series_kurtosis,
            'beyond1std':series_beyond1std,
            'mag_percentiles':series_mag_percentiles,
            'mag_iqr': series_mag_percentiles[8] - series_mag_percentiles[3],
        }


    else:
        LOGERROR('not enough detections in this magseries '
                 'to calculate light curve moments')
        return None