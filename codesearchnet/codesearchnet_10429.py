def check_mdpargs(d):
    """Check if any arguments remain in dict *d*."""
    if len(d) > 0:
        wmsg = "Unprocessed mdp option are interpreted as options for grompp:\n"+str(d)
        logger.warn(wmsg)
        warnings.warn(wmsg, category=UsageWarning)
    return len(d) == 0