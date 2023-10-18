def pdw_worker(task):
    '''
    This is the parallel worker for the function below.

    task[0] = frequency for this worker
    task[1] = times array
    task[2] = mags array
    task[3] = fold_time
    task[4] = j_range
    task[5] = keep_threshold_1
    task[6] = keep_threshold_2
    task[7] = phasebinsize

    we don't need errs for the worker.

    '''

    frequency = task[0]
    times, modmags = task[1], task[2]
    fold_time = task[3]
    j_range = range(task[4])
    keep_threshold_1 = task[5]
    keep_threshold_2 = task[6]
    phasebinsize = task[7]


    try:

        period = 1.0/frequency

        # use the common phaser to phase and sort the mag
        phased = phase_magseries(times,
                                 modmags,
                                 period,
                                 fold_time,
                                 wrap=False,
                                 sort=True)

        # bin in phase if requested, this turns this into a sort of PDM method
        if phasebinsize is not None and phasebinsize > 0:
            bphased = pwd_phasebin(phased['phase'],
                                   phased['mags'],
                                   binsize=phasebinsize)
            phase_sorted = bphased[0]
            mod_mag_sorted = bphased[1]
            j_range = range(len(mod_mag_sorted) - 1)
        else:
            phase_sorted = phased['phase']
            mod_mag_sorted = phased['mags']

        # now calculate the string length
        rolledmags = nproll(mod_mag_sorted,1)
        rolledphases = nproll(phase_sorted,1)
        strings = (
            (rolledmags - mod_mag_sorted)*(rolledmags - mod_mag_sorted) +
            (rolledphases - phase_sorted)*(rolledphases - phase_sorted)
        )
        strings[0] = (
            ((mod_mag_sorted[0] - mod_mag_sorted[-1]) *
             (mod_mag_sorted[0] - mod_mag_sorted[-1])) +
            ((phase_sorted[0] - phase_sorted[-1] + 1) *
             (phase_sorted[0] - phase_sorted[-1] + 1))
        )
        strlen = npsum(npsqrt(strings))

        if (keep_threshold_1 < strlen < keep_threshold_2):
            p_goodflag  = True
        else:
            p_goodflag = False

        return (period, strlen, p_goodflag)

    except Exception as e:

        LOGEXCEPTION('error in DWP')
        return(period, npnan, False)