def lightcurve_flux_measures(ftimes, fmags, ferrs, magsarefluxes=False):
    '''This calculates percentiles and percentile ratios of the flux.

    Parameters
    ----------

    ftimes,fmags,ferrs : np.array
        The input mag/flux time-series with all non-finite elements removed.

    magsarefluxes : bool
        If the `fmags` array actually contains fluxes, will not convert `mags`
        to fluxes before calculating the percentiles.

    Returns
    -------

    dict
        A dict with all of the light curve flux percentiles and percentile
        ratios calculated.

    '''

    ndet = len(fmags)

    if ndet > 9:

        # get the fluxes
        if magsarefluxes:
            series_fluxes = fmags
        else:
            series_fluxes = 10.0**(-0.4*fmags)

        series_flux_median = npmedian(series_fluxes)

        # get the percent_amplitude for the fluxes
        series_flux_percent_amplitude = (
            npmax(npabs(series_fluxes))/series_flux_median
        )

        # get the flux percentiles
        series_flux_percentiles = nppercentile(
            series_fluxes,
            [5.0,10,17.5,25,32.5,40,60,67.5,75,82.5,90,95]
        )
        series_frat_595 = (
            series_flux_percentiles[-1] - series_flux_percentiles[0]
        )
        series_frat_1090 = (
            series_flux_percentiles[-2] - series_flux_percentiles[1]
        )
        series_frat_175825 = (
            series_flux_percentiles[-3] - series_flux_percentiles[2]
        )
        series_frat_2575 = (
            series_flux_percentiles[-4] - series_flux_percentiles[3]
        )
        series_frat_325675 = (
            series_flux_percentiles[-5] - series_flux_percentiles[4]
        )
        series_frat_4060 = (
            series_flux_percentiles[-6] - series_flux_percentiles[5]
        )

        # calculate the flux percentile ratios
        series_flux_percentile_ratio_mid20 = series_frat_4060/series_frat_595
        series_flux_percentile_ratio_mid35 = series_frat_325675/series_frat_595
        series_flux_percentile_ratio_mid50 = series_frat_2575/series_frat_595
        series_flux_percentile_ratio_mid65 = series_frat_175825/series_frat_595
        series_flux_percentile_ratio_mid80 = series_frat_1090/series_frat_595

        # calculate the ratio of F595/median flux
        series_percent_difference_flux_percentile = (
            series_frat_595/series_flux_median
        )
        series_percentile_magdiff = -2.5*nplog10(
            series_percent_difference_flux_percentile
        )

        return {
            'flux_median':series_flux_median,
            'flux_percent_amplitude':series_flux_percent_amplitude,
            'flux_percentiles':series_flux_percentiles,
            'flux_percentile_ratio_mid20':series_flux_percentile_ratio_mid20,
            'flux_percentile_ratio_mid35':series_flux_percentile_ratio_mid35,
            'flux_percentile_ratio_mid50':series_flux_percentile_ratio_mid50,
            'flux_percentile_ratio_mid65':series_flux_percentile_ratio_mid65,
            'flux_percentile_ratio_mid80':series_flux_percentile_ratio_mid80,
            'percent_difference_flux_percentile':series_percentile_magdiff,
        }


    else:

        LOGERROR('not enough detections in this magseries '
                 'to calculate flux measures')
        return None