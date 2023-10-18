def add_flare_model(flareparams,
                    times,
                    mags,
                    errs):
    '''This adds a flare model function to the input magnitude/flux time-series.

    Parameters
    ----------

    flareparams : list of float
        This defines the flare model::

            [amplitude,
             flare_peak_time,
             rise_gaussian_stdev,
             decay_time_constant]

        where:

        `amplitude`: the maximum flare amplitude in mags or flux. If flux, then
        amplitude should be positive. If mags, amplitude should be negative.

        `flare_peak_time`: time at which the flare maximum happens.

        `rise_gaussian_stdev`: the stdev of the gaussian describing the rise of
        the flare.

        `decay_time_constant`: the time constant of the exponential fall of the
        flare.

    times,mags,errs : np.array
        The input time-series of measurements and associated errors for which
        the model will be generated. The times will be used to generate
        model mags.

    magsarefluxes : bool
        Sets the correct direction of the flare amplitude (+ve) for fluxes if
        True and for mags (-ve) if False.

    Returns
    -------

    dict
        A dict of the form below is returned::

        {'times': the original times array
         'mags': the original mags + the flare model mags evaluated at times,
         'errs': the original errs array,
         'flareparams': the input list of flare params}

    '''

    modelmags, ftimes, fmags, ferrs = flares.flare_model(
        flareparams,
        times,
        mags,
        errs
    )

    return {'times':times,
            'mags':mags + modelmags,
            'errs':errs,
            'flareparams':flareparams}