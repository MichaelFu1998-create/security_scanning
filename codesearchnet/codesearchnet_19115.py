def show_progress(name, **kwargs):
    '''
    Sets up a :class:`ProgressBarHandler` to handle progess logs for
    a given module.

    Parameters
    ----------
    name : string
        The module name of the progress logger to use. For example,
        :class:`skl_groups.divergences.KNNDivergenceEstimator`
        uses ``'skl_groups.divergences.knn.progress'``.

    * : anything
        Other keyword arguments are passed to the :class:`ProgressBarHandler`.
    '''
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(ProgressBarHandler(**kwargs))