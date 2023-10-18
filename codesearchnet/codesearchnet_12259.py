def nonperiodic_lightcurve_features(times, mags, errs, magsarefluxes=False):
    '''This calculates the following nonperiodic features of the light curve,
    listed in Richards, et al. 2011):

    - amplitude
    - beyond1std
    - flux_percentile_ratio_mid20
    - flux_percentile_ratio_mid35
    - flux_percentile_ratio_mid50
    - flux_percentile_ratio_mid65
    - flux_percentile_ratio_mid80
    - linear_trend
    - max_slope
    - median_absolute_deviation
    - median_buffer_range_percentage
    - pair_slope_trend
    - percent_amplitude
    - percent_difference_flux_percentile
    - skew
    - stdev
    - timelength
    - mintime
    - maxtime

    Parameters
    ----------

    times,mags,errs : np.array
        The input mag/flux time-series to process.

    magsarefluxes : bool
        If True, will treat values in `mags` as fluxes instead of magnitudes.

    Returns
    -------

    dict
        A dict containing all of the features listed above.

    '''

    # remove nans first
    finiteind = npisfinite(times) & npisfinite(mags) & npisfinite(errs)
    ftimes, fmags, ferrs = times[finiteind], mags[finiteind], errs[finiteind]

    # remove zero errors
    nzind = npnonzero(ferrs)
    ftimes, fmags, ferrs = ftimes[nzind], fmags[nzind], ferrs[nzind]

    ndet = len(fmags)

    if ndet > 9:

        # calculate the moments
        moments = lightcurve_moments(ftimes, fmags, ferrs)

        # calculate the flux measures
        fluxmeasures = lightcurve_flux_measures(ftimes, fmags, ferrs,
                                                magsarefluxes=magsarefluxes)

        # calculate the point-to-point measures
        ptpmeasures = lightcurve_ptp_measures(ftimes, fmags, ferrs)

        # get the length in time
        mintime, maxtime = npmin(ftimes), npmax(ftimes)
        timelength = maxtime - mintime

        # get the amplitude
        series_amplitude = 0.5*(npmax(fmags) - npmin(fmags))

        # calculate the linear fit to the entire mag series
        fitcoeffs = nppolyfit(ftimes, fmags, 1, w=1.0/(ferrs*ferrs))
        series_linear_slope = fitcoeffs[1]

        # roll fmags by 1
        rolled_fmags = nproll(fmags,1)

        # calculate the magnitude ratio (from the WISE paper)
        series_magratio = (
            (npmax(fmags) - moments['median']) / (npmax(fmags) - npmin(fmags) )
        )

        # this is the dictionary returned containing all the measures
        measures = {
            'ndet':fmags.size,
            'mintime':mintime,
            'maxtime':maxtime,
            'timelength':timelength,
            'amplitude':series_amplitude,
            'ndetobslength_ratio':ndet/timelength,
            'linear_fit_slope':series_linear_slope,
            'magnitude_ratio':series_magratio,
        }
        if moments:
            measures.update(moments)
        if ptpmeasures:
            measures.update(ptpmeasures)
        if fluxmeasures:
            measures.update(fluxmeasures)

        return measures

    else:

        LOGERROR('not enough detections in this magseries '
                 'to calculate non-periodic features')
        return None