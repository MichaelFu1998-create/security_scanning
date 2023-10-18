def invgauss_eclipses_func(ebparams, times, mags, errs):
    '''This returns a double eclipse shaped function.

    Suitable for first order modeling of eclipsing binaries.

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

        - for magnitudes -> pdepth should be < 0
        - for fluxes     -> pdepth should be > 0

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

    (modelmags, phase, ptimes, pmags, perrs) : tuple
        Returns the model mags and phase values. Also returns the input `times`,
        `mags`, and `errs` sorted by the model's phase.

    '''

    (period, epoch, pdepth, pduration, depthratio, secondaryphase) = ebparams

    # generate the phases
    iphase = (times - epoch)/period
    iphase = iphase - np.floor(iphase)

    phasesortind = np.argsort(iphase)
    phase = iphase[phasesortind]
    ptimes = times[phasesortind]
    pmags = mags[phasesortind]
    perrs = errs[phasesortind]

    zerolevel = np.median(pmags)
    modelmags = np.full_like(phase, zerolevel)

    primaryecl_amp = -pdepth
    secondaryecl_amp = -pdepth * depthratio

    primaryecl_std = pduration/5.0    # we use 5-sigma as full-width -> duration
    secondaryecl_std = pduration/5.0  # secondary eclipse has the same duration

    halfduration = pduration/2.0


    # phase indices
    primary_eclipse_ingress = (
        (phase >= (1.0 - halfduration)) & (phase <= 1.0)
    )
    primary_eclipse_egress = (
        (phase >= 0.0) & (phase <= halfduration)
    )

    secondary_eclipse_phase = (
        (phase >= (secondaryphase - halfduration)) &
        (phase <= (secondaryphase + halfduration))
    )

    # put in the eclipses
    modelmags[primary_eclipse_ingress] = (
        zerolevel + _gaussian(phase[primary_eclipse_ingress],
                              primaryecl_amp,
                              1.0,
                              primaryecl_std)
    )
    modelmags[primary_eclipse_egress] = (
        zerolevel + _gaussian(phase[primary_eclipse_egress],
                              primaryecl_amp,
                              0.0,
                              primaryecl_std)
    )
    modelmags[secondary_eclipse_phase] = (
        zerolevel + _gaussian(phase[secondary_eclipse_phase],
                              secondaryecl_amp,
                              secondaryphase,
                              secondaryecl_std)
    )

    return modelmags, phase, ptimes, pmags, perrs