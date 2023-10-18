def invgauss_eclipses_residual(ebparams, times, mags, errs):
    '''This returns the residual between the modelmags and the actual mags.

    Parameters
    ----------

    ebparams : list of float
        This contains the parameters for the eclipsing binary::

            ebparams = [period (time),
                        epoch (time),
                        pdepth: primary eclipse depth (mags),
                        pduration: primary eclipse duration (phase),
                        psdepthratio: primary-secondary eclipse depth ratio,
                        secondaryphase: center phase of the secondary eclipse]

        `period` is the period in days.

        `epoch` is the time of minimum in JD.

        `pdepth` is the depth of the primary eclipse.

        - for magnitudes -> `pdepth` should be < 0
        - for fluxes     -> `pdepth` should be > 0

        `pduration` is the length of the primary eclipse in phase.

        `psdepthratio` is the ratio in the eclipse depths:
        `depth_secondary/depth_primary`. This is generally the same as the ratio
        of the `T_effs` of the two stars.

        `secondaryphase` is the phase at which the minimum of the secondary
        eclipse is located. This effectively parameterizes eccentricity.

        All of these will then have fitted values after the fit is done.

    times,mags,errs : np.array
        The input time-series of measurements and associated errors for which
        the eclipse model will be generated. The times will be used to generate
        model mags, and the input `times`, `mags`, and `errs` will be resorted
        by model phase and returned.

    Returns
    -------

    np.array
        The residuals between the input `mags` and generated `modelmags`,
        weighted by the measurement errors in `errs`.

    '''

    modelmags, phase, ptimes, pmags, perrs = (
        invgauss_eclipses_func(ebparams, times, mags, errs)
    )

    # this is now a weighted residual taking into account the measurement err
    return (pmags - modelmags)/perrs