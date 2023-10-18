def _parallel_bls_worker(task):
    '''
    This wraps Astropy's BoxLeastSquares for use with bls_parallel_pfind below.

    `task` is a tuple::

        task[0] = times
        task[1] = mags
        task[2] = errs
        task[3] = magsarefluxes

        task[4] = minfreq
        task[5] = nfreq
        task[6] = stepsize

        task[7] = ndurations
        task[8] = mintransitduration
        task[9] = maxtransitduration

        task[10] = blsobjective
        task[11] = blsmethod
        task[12] = blsoversample

    '''

    try:

        times, mags, errs = task[:3]
        magsarefluxes = task[3]

        minfreq, nfreq, stepsize = task[4:7]

        ndurations, mintransitduration, maxtransitduration = task[7:10]

        blsobjective, blsmethod, blsoversample = task[10:]

        frequencies = minfreq + nparange(nfreq)*stepsize
        periods = 1.0/frequencies

        # astropy's BLS requires durations in units of time
        durations = nplinspace(mintransitduration*periods.min(),
                               maxtransitduration*periods.min(),
                               ndurations)

        # set up the correct units for the BLS model
        if magsarefluxes:

            blsmodel = BoxLeastSquares(
                times*u.day,
                mags*u.dimensionless_unscaled,
                dy=errs*u.dimensionless_unscaled
            )

        else:

            blsmodel = BoxLeastSquares(
                times*u.day,
                mags*u.mag,
                dy=errs*u.mag
            )

        blsresult = blsmodel.power(
            periods*u.day,
            durations*u.day,
            objective=blsobjective,
            method=blsmethod,
            oversample=blsoversample
        )

        return {
            'blsresult': blsresult,
            'blsmodel': blsmodel,
            'durations': durations,
            'power': nparray(blsresult.power)
        }

    except Exception as e:

        LOGEXCEPTION('BLS for frequency chunk: (%.6f, %.6f) failed.' %
                     (frequencies[0], frequencies[-1]))

        return {
            'blsresult': None,
            'blsmodel': None,
            'durations': durations,
            'power': nparray([npnan for x in range(nfreq)]),
        }