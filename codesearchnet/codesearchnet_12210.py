def fourier_fit_magseries(times, mags, errs, period,
                          fourierorder=None,
                          fourierparams=None,
                          sigclip=3.0,
                          magsarefluxes=False,
                          plotfit=False,
                          ignoreinitfail=True,
                          verbose=True):
    '''This fits a Fourier series to a mag/flux time series.

    Parameters
    ----------

    times,mags,errs : np.array
        The input mag/flux time-series to fit a Fourier cosine series to.

    period : float
        The period to use for the Fourier fit.

    fourierorder : None or int
        If this is an int, will be interpreted as the Fourier order of the
        series to fit to the input mag/flux times-series. If this is None and
        `fourierparams` is specified, `fourierparams` will be used directly to
        generate the fit Fourier series. If `fourierparams` is also None, this
        function will try to fit a Fourier cosine series of order 3 to the
        mag/flux time-series.

    fourierparams : list of floats or None
        If this is specified as a list of floats, it must be of the form below::

            [fourier_amp1, fourier_amp2, fourier_amp3,...,fourier_ampN,
             fourier_phase1, fourier_phase2, fourier_phase3,...,fourier_phaseN]

        to specify a Fourier cosine series of order N. If this is None and
        `fourierorder` is specified, the Fourier order specified there will be
        used to construct the Fourier cosine series used to fit the input
        mag/flux time-series. If both are None, this function will try to fit a
        Fourier cosine series of order 3 to the input mag/flux time-series.

    sigclip : float or int or sequence of two floats/ints or None
        If a single float or int, a symmetric sigma-clip will be performed using
        the number provided as the sigma-multiplier to cut out from the input
        time-series.

        If a list of two ints/floats is provided, the function will perform an
        'asymmetric' sigma-clip. The first element in this list is the sigma
        value to use for fainter flux/mag values; the second element in this
        list is the sigma value to use for brighter flux/mag values. For
        example, `sigclip=[10., 3.]`, will sigclip out greater than 10-sigma
        dimmings and greater than 3-sigma brightenings. Here the meaning of
        "dimming" and "brightening" is set by *physics* (not the magnitude
        system), which is why the `magsarefluxes` kwarg must be correctly set.

        If `sigclip` is None, no sigma-clipping will be performed, and the
        time-series (with non-finite elems removed) will be passed through to
        the output.

    magsarefluxes : bool
        If True, will treat the input values of `mags` as fluxes for purposes of
        plotting the fit and sig-clipping.

    plotfit : str or False
        If this is a string, this function will make a plot for the fit to the
        mag/flux time-series and writes the plot to the path specified here.

    ignoreinitfail : bool
        If this is True, ignores the initial failure to find a set of optimized
        Fourier parameters using the global optimization function and proceeds
        to do a least-squares fit anyway.

    verbose : bool
        If True, will indicate progress and warn of any problems.

    Returns
    -------

    dict
        This function returns a dict containing the model fit parameters, the
        minimized chi-sq value and the reduced chi-sq value. The form of this
        dict is mostly standardized across all functions in this module::

            {
                'fittype':'fourier',
                'fitinfo':{
                    'finalparams': the list of final model fit params,
                    'leastsqfit':the full tuple returned by scipy.leastsq,
                    'fitmags': the model fit mags,
                    'fitepoch': the epoch of minimum light for the fit,
                    ... other fit function specific keys ...
                },
                'fitchisq': the minimized value of the fit's chi-sq,
                'fitredchisq':the reduced chi-sq value,
                'fitplotfile': the output fit plot if fitplot is not None,
                'magseries':{
                    'times':input times in phase order of the model,
                    'phase':the phases of the model mags,
                    'mags':input mags/fluxes in the phase order of the model,
                    'errs':errs in the phase order of the model,
                    'magsarefluxes':input value of magsarefluxes kwarg
                }
            }

        NOTE: the returned value of 'fitepoch' in the 'fitinfo' dict returned by
        this function is the time value of the first observation since this is
        where the LC is folded for the fit procedure. To get the actual time of
        minimum epoch as calculated by a spline fit to the phased LC, use the
        key 'actual_fitepoch' in the 'fitinfo' dict.

    '''

    stimes, smags, serrs = sigclip_magseries(times, mags, errs,
                                             sigclip=sigclip,
                                             magsarefluxes=magsarefluxes)

    # get rid of zero errs
    nzind = npnonzero(serrs)
    stimes, smags, serrs = stimes[nzind], smags[nzind], serrs[nzind]

    phase, pmags, perrs, ptimes, mintime = (
        get_phased_quantities(stimes, smags, serrs, period)
    )


    # get the fourier order either from the scalar order kwarg...
    if fourierorder and fourierorder > 0 and not fourierparams:

        fourieramps = [0.6] + [0.2]*(fourierorder - 1)
        fourierphas = [0.1] + [0.1]*(fourierorder - 1)
        fourierparams = fourieramps + fourierphas

    # or from the fully specified coeffs vector
    elif not fourierorder and fourierparams:

        fourierorder = int(len(fourierparams)/2)

    else:
        LOGWARNING('specified both/neither Fourier order AND Fourier coeffs, '
                   'using default Fourier order of 3')
        fourierorder = 3
        fourieramps = [0.6] + [0.2]*(fourierorder - 1)
        fourierphas = [0.1] + [0.1]*(fourierorder - 1)
        fourierparams = fourieramps + fourierphas

    if verbose:
        LOGINFO('fitting Fourier series of order %s to '
                'mag series with %s observations, '
                'using period %.6f, folded at %.6f' % (fourierorder,
                                                       len(phase),
                                                       period,
                                                       mintime))

    # initial minimize call to find global minimum in chi-sq
    initialfit = spminimize(_fourier_chisq,
                            fourierparams,
                            method='BFGS',
                            args=(phase, pmags, perrs))

    # make sure this initial fit succeeds before proceeding
    if initialfit.success or ignoreinitfail:

        if verbose:
            LOGINFO('initial fit done, refining...')

        leastsqparams = initialfit.x

        try:
            leastsqfit = spleastsq(_fourier_residual,
                                   leastsqparams,
                                   args=(phase, pmags))
        except Exception as e:
            leastsqfit = None

        # if the fit succeeded, then we can return the final parameters
        if leastsqfit and leastsqfit[-1] in (1,2,3,4):

            finalparams = leastsqfit[0]

            # calculate the chisq and reduced chisq
            fitmags = _fourier_func(finalparams, phase, pmags)

            fitchisq = npsum(
                ((fitmags - pmags)*(fitmags - pmags)) / (perrs*perrs)
            )

            fitredchisq = fitchisq/(len(pmags) - len(finalparams) - 1)

            if verbose:
                LOGINFO(
                    'final fit done. chisq = %.5f, reduced chisq = %.5f' %
                    (fitchisq,fitredchisq)
                )

            # figure out the time of light curve minimum (i.e. the fit epoch)
            # this is when the fit mag is maximum (i.e. the faintest)
            # or if magsarefluxes = True, then this is when fit flux is minimum
            if not magsarefluxes:
                fitmagminind = npwhere(fitmags == npmax(fitmags))
            else:
                fitmagminind = npwhere(fitmags == npmin(fitmags))
            if len(fitmagminind[0]) > 1:
                fitmagminind = (fitmagminind[0][0],)

            # assemble the returndict
            returndict = {
                'fittype':'fourier',
                'fitinfo':{
                    'fourierorder':fourierorder,
                    'finalparams':finalparams,
                    'initialfit':initialfit,
                    'leastsqfit':leastsqfit,
                    'fitmags':fitmags,
                    'fitepoch':mintime,
                    'actual_fitepoch':ptimes[fitmagminind]
                },
                'fitchisq':fitchisq,
                'fitredchisq':fitredchisq,
                'fitplotfile':None,
                'magseries':{
                    'times':ptimes,
                    'phase':phase,
                    'mags':pmags,
                    'errs':perrs,
                    'magsarefluxes':magsarefluxes
                },
            }

            # make the fit plot if required
            if plotfit and isinstance(plotfit, str):

                make_fit_plot(phase, pmags, perrs, fitmags,
                              period, mintime, mintime,
                              plotfit,
                              magsarefluxes=magsarefluxes)

                returndict['fitplotfile'] = plotfit

            return returndict

        # if the leastsq fit did not succeed, return Nothing
        else:
            LOGERROR('fourier-fit: least-squared fit to the light curve failed')
            return {
                'fittype':'fourier',
                'fitinfo':{
                    'fourierorder':fourierorder,
                    'finalparams':None,
                    'initialfit':initialfit,
                    'leastsqfit':None,
                    'fitmags':None,
                    'fitepoch':None
                },
                'fitchisq':npnan,
                'fitredchisq':npnan,
                'fitplotfile':None,
                'magseries':{
                    'times':ptimes,
                    'phase':phase,
                    'mags':pmags,
                    'errs':perrs,
                    'magsarefluxes':magsarefluxes
                }
            }


    # if the fit didn't succeed, we can't proceed
    else:

        LOGERROR('initial Fourier fit did not succeed, '
                 'reason: %s, returning scipy OptimizeResult'
                 % initialfit.message)

        return {
            'fittype':'fourier',
            'fitinfo':{
                'fourierorder':fourierorder,
                'finalparams':None,
                'initialfit':initialfit,
                'leastsqfit':None,
                'fitmags':None,
                'fitepoch':None
            },
            'fitchisq':npnan,
            'fitredchisq':npnan,
            'fitplotfile':None,
            'magseries':{
                'times':ptimes,
                'phase':phase,
                'mags':pmags,
                'errs':perrs,
                'magsarefluxes':magsarefluxes
            }
        }