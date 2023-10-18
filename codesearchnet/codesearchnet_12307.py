def variable_index_gridsearch_magbin(simbasedir,
                                     stetson_stdev_range=(1.0,20.0),
                                     inveta_stdev_range=(1.0,20.0),
                                     iqr_stdev_range=(1.0,20.0),
                                     ngridpoints=32,
                                     ngridworkers=None):
    '''This runs a variable index grid search per magbin.

    For each magbin, this does a grid search using the stetson and inveta ranges
    provided and tries to optimize the Matthews Correlation Coefficient (best
    value is +1.0), indicating the best possible separation of variables
    vs. nonvariables. The thresholds on these two variable indexes that produce
    the largest coeff for the collection of fake LCs will probably be the ones
    that work best for actual variable classification on the real LCs.

    https://en.wikipedia.org/wiki/Matthews_correlation_coefficient

    For each grid-point, calculates the true positives, false positives, true
    negatives, false negatives. Then gets the precision and recall, confusion
    matrix, and the ROC curve for variable vs. nonvariable.

    Once we've identified the best thresholds to use, we can then calculate
    variable object numbers:

    - as a function of magnitude
    - as a function of period
    - as a function of number of detections
    - as a function of amplitude of variability


    Writes everything back to `simbasedir/fakevar-recovery.pkl`. Use the
    plotting function below to make plots for the results.

    Parameters
    ----------

    simbasedir : str
        The directory where the fake LCs are located.

    stetson_stdev_range : sequence of 2 floats
        The min and max values of the Stetson J variability index to generate a
        grid over these to test for the values of this index that produce the
        'best' recovery rate for the injected variable stars.

    inveta_stdev_range : sequence of 2 floats
        The min and max values of the 1/eta variability index to generate a
        grid over these to test for the values of this index that produce the
        'best' recovery rate for the injected variable stars.

    iqr_stdev_range : sequence of 2 floats
        The min and max values of the IQR variability index to generate a
        grid over these to test for the values of this index that produce the
        'best' recovery rate for the injected variable stars.

    ngridpoints : int
        The number of grid points for each variability index grid. Remember that
        this function will be searching in 3D and will require lots of time to
        run if ngridpoints is too large.

        For the default number of grid points and 25000 simulated light curves,
        this takes about 3 days to run on a 40 (effective) core machine with 2 x
        Xeon E5-2650v3 CPUs.

    ngridworkers : int or None
        The number of parallel grid search workers that will be launched.

    Returns
    -------

    dict
        The returned dict contains a list of recovery stats for each magbin and
        each grid point in the variability index grids that were used. This dict
        can be passed to the plotting function below to plot the results.

    '''

    # make the output directory where all the pkls from the variability
    # threshold runs will go
    outdir = os.path.join(simbasedir,'recvar-threshold-pkls')
    if not os.path.exists(outdir):
        os.mkdir(outdir)

    # get the info from the simbasedir
    with open(os.path.join(simbasedir, 'fakelcs-info.pkl'),'rb') as infd:
        siminfo = pickle.load(infd)

    # get the column defs for the fakelcs
    timecols = siminfo['timecols']
    magcols = siminfo['magcols']
    errcols = siminfo['errcols']

    # get the magbinmedians to use for the recovery processing
    magbinmedians = siminfo['magrms'][magcols[0]]['binned_sdssr_median']

    # generate the grids for stetson and inveta
    stetson_grid = np.linspace(stetson_stdev_range[0],
                               stetson_stdev_range[1],
                               num=ngridpoints)
    inveta_grid = np.linspace(inveta_stdev_range[0],
                              inveta_stdev_range[1],
                              num=ngridpoints)
    iqr_grid = np.linspace(iqr_stdev_range[0],
                           iqr_stdev_range[1],
                           num=ngridpoints)

    # generate the grid
    stet_inveta_iqr_grid = []
    for stet in stetson_grid:
        for inveta in inveta_grid:
            for iqr in iqr_grid:
                grid_point = [stet, inveta, iqr]
                stet_inveta_iqr_grid.append(grid_point)

    # the output dict
    grid_results = {'stetson_grid':stetson_grid,
                    'inveta_grid':inveta_grid,
                    'iqr_grid':iqr_grid,
                    'stet_inveta_iqr_grid':stet_inveta_iqr_grid,
                    'magbinmedians':magbinmedians,
                    'timecols':timecols,
                    'magcols':magcols,
                    'errcols':errcols,
                    'simbasedir':os.path.abspath(simbasedir),
                    'recovery':[]}


    # set up the pool
    pool = mp.Pool(ngridworkers)

    # run the grid search per magbinmedian
    for magbinmedian in magbinmedians:

        LOGINFO('running stetson J-inveta grid-search '
                'for magbinmedian = %.3f...' % magbinmedian)

        tasks = [(simbasedir, gp, magbinmedian) for gp in stet_inveta_iqr_grid]
        thisbin_results = pool.map(magbin_varind_gridsearch_worker, tasks)
        grid_results['recovery'].append(thisbin_results)

    pool.close()
    pool.join()


    LOGINFO('done.')
    with open(os.path.join(simbasedir,
                           'fakevar-recovery-per-magbin.pkl'),'wb') as outfd:
        pickle.dump(grid_results,outfd,pickle.HIGHEST_PROTOCOL)

    return grid_results