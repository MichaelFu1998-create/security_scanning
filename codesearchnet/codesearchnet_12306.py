def magbin_varind_gridsearch_worker(task):
    '''
    This is a parallel grid search worker for the function below.

    '''

    simbasedir, gridpoint, magbinmedian = task

    try:
        res = get_recovered_variables_for_magbin(simbasedir,
                                                 magbinmedian,
                                                 stetson_stdev_min=gridpoint[0],
                                                 inveta_stdev_min=gridpoint[1],
                                                 iqr_stdev_min=gridpoint[2],
                                                 statsonly=True)
        return res
    except Exception as e:
        LOGEXCEPTION('failed to get info for %s' % gridpoint)
        return None