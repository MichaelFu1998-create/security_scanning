def mask_signal(times, mags, errs,
                signalperiod,
                signalepoch,
                magsarefluxes=False,
                maskphases=(0,0,0.5,1.0),
                maskphaselength=0.1,
                plotfit=None,
                plotfitphasedlconly=True,
                sigclip=30.0):
    '''This removes repeating signals in the magnitude time series.

    Useful for masking planetary transit signals in light curves to search for
    other variability.

    A small worked example of using this and `prewhiten_magseries` above:

    https://github.com/waqasbhatti/astrobase/issues/77#issuecomment-463803558

    Parameters
    ----------

    times,mags,errs : np.array
        The input mag/flux time-series to run the masking on.

    signalperiod : float
        The period of the signal to mask.

    signalepoch : float
        The epoch of the signal to mask.

    magsarefluxes : bool
        Set to True if `mags` is actually an array of fluxes.

    maskphases : sequence of floats
        This defines which phase values will be masked. For each item in this
        sequence, this function will mask a length of phase given by
        `maskphaselength` centered on each `maskphases` value, and remove all LC
        points in these regions from the light curve.

    maskphaselength : float
        The length in phase to mask for each phase value provided in
        `maskphases`.

    plotfit : str or None
        If provided as a str, indicates the output plot file.

    plotfitphasedlconly : bool
        If True, will only plot the effect of masking the signal as requested on
        the phased LC. If False, will also plot the unphased LC.

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

    '''

    stimes, smags, serrs = sigclip_magseries(times, mags, errs,
                                             sigclip=sigclip,
                                             magsarefluxes=magsarefluxes)


    # now phase the light curve using the period and epoch provided
    phases = (
        (stimes - signalepoch)/signalperiod -
        np.floor((stimes - signalepoch)/signalperiod)
    )

    # mask the requested phases using the mask length (in phase units)
    # this gets all the masks into one array
    masks = np.array([(np.abs(phases - x) > maskphaselength)
                      for x in maskphases])
    # this flattens the masks to a single array for all combinations
    masks = np.all(masks,axis=0)

    # apply the mask to the times, mags, and errs
    mphases = phases[masks]
    mtimes = stimes[masks]
    mmags = smags[masks]
    merrs = serrs[masks]

    returndict = {'mphases':mphases,
                  'mtimes':mtimes,
                  'mmags':mmags,
                  'merrs':merrs}

    # make the fit plot if required
    if plotfit and isinstance(plotfit, str) or isinstance(plotfit, Strio):

        if plotfitphasedlconly:
            plt.figure(figsize=(10,4.8))
        else:
            plt.figure(figsize=(16,9.6))

        if plotfitphasedlconly:

            # phased series before whitening
            plt.subplot(121)
            plt.plot(phases,smags,
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
            plt.title('phased LC before signal masking')

            # phased series after whitening
            plt.subplot(122)
            plt.plot(mphases,mmags,
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
            plt.title('phased LC after signal masking')

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
            plt.title('LC before signal masking')

            # time series after whitening
            plt.subplot(222)
            plt.plot(mtimes,mmags,
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
            plt.title('LC after signal masking')

            # phased series before whitening
            plt.subplot(223)
            plt.plot(phases,smags,
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
            plt.title('phased LC before signal masking')

            # phased series after whitening
            plt.subplot(224)
            plt.plot(mphases,mmags,
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
            plt.title('phased LC after signal masking')

        plt.tight_layout()
        plt.savefig(plotfit, format='png', pad_inches=0.0)
        plt.close()

        if isinstance(plotfit, str) or isinstance(plotfit, Strio):
            returndict['fitplotfile'] = plotfit


    return returndict