def parallel_periodicvar_recovery(simbasedir,
                                  period_tolerance=1.0e-3,
                                  liststartind=None,
                                  listmaxobjects=None,
                                  nworkers=None):
    '''This is a parallel driver for `periodicvar_recovery`.

    Parameters
    ----------

    simbasedir : str
        The base directory where all of the fake LCs and period-finding results
        are.

    period_tolerance : float
        The maximum difference that this function will consider between an
        actual period (or its aliases) and a recovered period to consider it as
        as a 'recovered' period.

    liststartindex : int
        The starting index of processing. This refers to the filename list
        generated by running `glob.glob` on the period-finding result pickles in
        `simbasedir/periodfinding`.

    listmaxobjects : int
        The maximum number of objects to process in this run. Use this with
        `liststartindex` to effectively distribute working on a large list of
        input period-finding result pickles over several sessions or machines.

    nperiodworkers : int
        This is the number of parallel period-finding worker processes to use.

    Returns
    -------

    str
        Returns the filename of the pickle produced containing all of the period
        recovery results.

    '''

    # figure out the periodfinding pickles directory
    pfpkldir = os.path.join(simbasedir,'periodfinding')

    if not os.path.exists(pfpkldir):
        LOGERROR('no "periodfinding" subdirectory in %s, can\'t continue' %
                 simbasedir)
        return None

    # find all the periodfinding pickles
    pfpkl_list = glob.glob(os.path.join(pfpkldir,'*periodfinding*pkl*'))

    if len(pfpkl_list) > 0:

        if liststartind:
            pfpkl_list = pfpkl_list[liststartind:]

        if listmaxobjects:
            pfpkl_list = pfpkl_list[:listmaxobjects]

        tasks = [(x, simbasedir, period_tolerance) for x in pfpkl_list]

        pool = mp.Pool(nworkers)
        results = pool.map(periodrec_worker, tasks)
        pool.close()
        pool.join()

        resdict = {x['objectid']:x for x in results if x is not None}

        actual_periodicvars = np.array(
            [x['objectid'] for x in results
             if (x is not None and x['actual_vartype'] in PERIODIC_VARTYPES)],
            dtype=np.unicode_
        )

        recovered_periodicvars = np.array(
            [x['objectid'] for x in results
             if (x is not None and 'actual' in x['best_recovered_status'])],
            dtype=np.unicode_
        )
        alias_twice_periodicvars = np.array(
            [x['objectid'] for x in results
             if (x is not None and 'twice' in x['best_recovered_status'])],
            dtype=np.unicode_
        )
        alias_half_periodicvars = np.array(
            [x['objectid'] for x in results
             if (x is not None and 'half' in x['best_recovered_status'])],
            dtype=np.unicode_
        )

        all_objectids = [x['objectid'] for x in results]

        outdict = {'simbasedir':os.path.abspath(simbasedir),
                   'objectids':all_objectids,
                   'period_tolerance':period_tolerance,
                   'actual_periodicvars':actual_periodicvars,
                   'recovered_periodicvars':recovered_periodicvars,
                   'alias_twice_periodicvars':alias_twice_periodicvars,
                   'alias_half_periodicvars':alias_half_periodicvars,
                   'details':resdict}

        outfile = os.path.join(simbasedir,'periodicvar-recovery.pkl')
        with open(outfile, 'wb') as outfd:
            pickle.dump(outdict, outfd, pickle.HIGHEST_PROTOCOL)

        return outdict

    else:

        LOGERROR(
            'no periodfinding result pickles found in %s, can\'t continue' %
            pfpkldir
        )
        return None