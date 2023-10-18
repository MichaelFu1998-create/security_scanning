def build_parallel(parallel_mode, quiet=True, processes=4,
                   user_modules=None, dispatcher_options=None):
    """initializes `Parallel`

    Parameters
    ----------
    parallel_mode : str
        "multiprocessing" (default), "htcondor" or "subprocess"
    quiet : bool, optional
        if True, progress bars will not be shown in the "multiprocessing" mode.
    process : int, optional
        The number of processes when ``parallel_mode`` is
        "multiprocessing"
    user_modules : list, optional
        The names of modules to be sent to worker nodes when
        parallel_mode is "htcondor"
    dispatcher_options : dict, optional
        Options to dispatcher

    Returns
    -------
    parallel
        an instance of the class `Parallel`

    """

    if user_modules is None:
        user_modules = [ ]

    if dispatcher_options is None:
        dispatcher_options = dict()

    dispatchers = ('subprocess', 'htcondor')
    parallel_modes = ('multiprocessing', ) + dispatchers
    default_parallel_mode = 'multiprocessing'

    if not parallel_mode in parallel_modes:
        logger = logging.getLogger(__name__)
        logger.warning('unknown parallel_mode "{}", use default "{}"'.format(
            parallel_mode, default_parallel_mode
        ))
        parallel_mode = default_parallel_mode

    if parallel_mode == 'multiprocessing':
        if quiet:
            atpbar.disable()
        return _build_parallel_multiprocessing(processes=processes)

    return _build_parallel_dropbox(
        parallel_mode=parallel_mode,
        user_modules=user_modules,
        dispatcher_options=dispatcher_options
    )