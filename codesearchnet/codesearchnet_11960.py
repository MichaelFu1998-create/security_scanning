def prewhiten_magseries(times, mags, errs,
                        whitenperiod,
                        whitenparams,
                        sigclip=3.0,
                        magsarefluxes=False,
                        plotfit=None,
                        plotfitphasedlconly=True,
                        rescaletomedian=True):
    '''Removes a periodic sinusoidal signal generated using whitenparams from
    the input magnitude time series.

    Parameters
    ----------

    times,mags,errs : np.array
        The input mag/flux time-series to prewhiten.

    whitenperiod : float
        The period of the sinusoidal signal to remove.

    whitenparams : list of floats
        This contains the Fourier amplitude and phase coefficients of the
        sinusoidal signal to remove::

            [ampl_1, ampl_2, ampl_3, ..., ampl_X,
             pha_1, pha_2, pha_3, ..., pha_X]

        where `X` is the Fourier order. These are usually the output of a
        previous Fourier fit to the light curve (from
        :py:func:`astrobase.lcfit.sinusoidal.fourier_fit_magseries` for
        example).

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
        If this is a string, this function will make a plot showing the effect
        of the pre-whitening on the mag/flux time-series and write the plot to
        the path specified here.

    plotfitphasedlconly : bool
        If True, will plot only the phased LC for showing the effect of
        pre-whitening, and skip plotting the unphased LC.

    rescaletomedian : bool
        If this is True, then we add back the constant median term of the
        magnitudes to the final pre-whitened mag series.

    Returns
    -------

    dict
        Returns a dict of the form::

            {'wtimes':times array after pre-whitening,
             'wphase':phase array after pre-whitening,
             'wmags':mags array after pre-whitening,
             'werrs':errs array after pre-whitening,
             'whitenparams':the input pre-whitening params used,
             'whitenperiod':the input pre-whitening period used,
             'fitplotfile':the output plot file if plotfit was set}

    '''

    stimes, smags, serrs = sigclip_magseries(times, mags, errs,
                                             sigclip=sigclip,
                                             magsarefluxes=magsarefluxes)

    median_mag = np.median(smags)


    # phase the mag series using the given period and epoch = min(stimes)
    mintime = np.min(stimes)

    # calculate the unsorted phase, then sort it
    iphase = (
        (stimes - mintime)/whitenperiod -
        np.floor((stimes - mintime)/whitenperiod)
    )
    phasesortind = np.argsort(iphase)

    # these are the final quantities to use for the Fourier fits
    phase = iphase[phasesortind]
    pmags = smags[phasesortind]
    perrs = serrs[phasesortind]

    # get the times sorted in phase order (useful to get the fit mag minimum
    # with respect to phase -- the light curve minimum)
    ptimes = stimes[phasesortind]

    # now subtract the harmonic series from the phased LC
    # these are still in phase order
    wmags = pmags - _fourier_func(whitenparams, phase, pmags)

    # resort everything by time order
    wtimeorder = np.argsort(ptimes)
    wtimes = ptimes[wtimeorder]
    wphase = phase[wtimeorder]
    wmags = wmags[wtimeorder]
    werrs = perrs[wtimeorder]

    if rescaletomedian:
        wmags = wmags + median_mag

    # prepare the returndict
    returndict = {'wtimes':wtimes,  # these are in the new time order
                  'wphase':wphase,
                  'wmags':wmags,
                  'werrs':werrs,
                  'whitenparams':whitenparams,
                  'whitenperiod':whitenperiod}


    # make the fit plot if required
    if plotfit and (isinstance(plotfit, str) or isinstance(plotfit, Strio)):

        if plotfitphasedlconly:
            plt.figure(figsize=(10,4.8))
        else:
            plt.figure(figsize=(16,9.6))

        if plotfitphasedlconly:

            # phased series before whitening
            plt.subplot(121)
            plt.plot(phase,pmags,
                     marker='.',
                     color='k',
                     linestyle='None',
                     markersize=2.0,
                     markeredgewidth=0)

            if not magsarefluxes:
                plt.gca().invert_yaxis()
                plt.ylabel('magnitude')
            else:
                plt.ylabel('fluxes')

            plt.xlabel('phase')
            plt.title('phased LC before pre-whitening')

            # phased series after whitening
            plt.subplot(122)
            plt.plot(wphase,wmags,
                     marker='.',
                     color='g',
                     linestyle='None',
                     markersize=2.0,
                     markeredgewidth=0)

            if not magsarefluxes:
                plt.gca().invert_yaxis()
                plt.ylabel('magnitude')
            else:
                plt.ylabel('fluxes')

            plt.xlabel('phase')
            plt.title('phased LC after pre-whitening')

        else:

            # time series before whitening
            plt.subplot(221)
            plt.plot(stimes,smags,
                     marker='.',
                     color='k',
                     linestyle='None',
                     markersize=2.0,
                     markeredgewidth=0)

            if not magsarefluxes:
                plt.gca().invert_yaxis()
                plt.ylabel('magnitude')
            else:
                plt.ylabel('fluxes')

            plt.xlabel('JD')
            plt.title('LC before pre-whitening')

            # time series after whitening
            plt.subplot(222)
            plt.plot(wtimes,wmags,
                     marker='.',
                     color='g',
                     linestyle='None',
                     markersize=2.0,
                     markeredgewidth=0)

            if not magsarefluxes:
                plt.gca().invert_yaxis()
                plt.ylabel('magnitude')
            else:
                plt.ylabel('fluxes')

            plt.xlabel('JD')
            plt.title('LC after pre-whitening with period: %.6f' % whitenperiod)

            # phased series before whitening
            plt.subplot(223)
            plt.plot(phase,pmags,
                     marker='.',
                     color='k',
                     linestyle='None',
                     markersize=2.0,
                     markeredgewidth=0)

            if not magsarefluxes:
                plt.gca().invert_yaxis()
                plt.ylabel('magnitude')
            else:
                plt.ylabel('fluxes')

            plt.xlabel('phase')
            plt.title('phased LC before pre-whitening')

            # phased series after whitening
            plt.subplot(224)
            plt.plot(wphase,wmags,
                     marker='.',
                     color='g',
                     linestyle='None',
                     markersize=2.0,
                     markeredgewidth=0)

            if not magsarefluxes:
                plt.gca().invert_yaxis()
                plt.ylabel('magnitude')
            else:
                plt.ylabel('fluxes')

            plt.xlabel('phase')
            plt.title('phased LC after pre-whitening')

        plt.tight_layout()
        plt.savefig(plotfit, format='png', pad_inches=0.0)
        plt.close()

        if isinstance(plotfit, str) or isinstance(plotfit, Strio):
            returndict['fitplotfile'] = plotfit

    return returndict