def _set_global_verbosity_level(is_verbose_output=False):
    """sets the global verbosity level for console and the jocker_lgr logger.

    :param bool is_verbose_output: should be output be verbose
    """
    global verbose_output
    # TODO: (IMPRV) only raise exceptions in verbose mode
    verbose_output = is_verbose_output
    if verbose_output:
        jocker_lgr.setLevel(logging.DEBUG)
    else:
        jocker_lgr.setLevel(logging.INFO)