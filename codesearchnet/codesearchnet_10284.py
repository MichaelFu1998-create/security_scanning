def get_double_or_single_prec_mdrun():
    """Return double precision ``mdrun`` or fall back to single precision.

    This convenience function tries :func:`gromacs.mdrun_d` first and
    if it cannot run it, falls back to :func:`gromacs.mdrun` (without
    further checking).

    .. versionadded:: 0.5.1
    """
    try:
        gromacs.mdrun_d(h=True, stdout=False, stderr=False)
        logger.debug("using double precision gromacs.mdrun_d")
        return gromacs.mdrun_d
    except (AttributeError, GromacsError, OSError):
        # fall back to mdrun if no double precision binary
        wmsg = "No 'mdrun_d' binary found so trying 'mdrun' instead.\n"\
            "(Note that energy minimization runs better with mdrun_d.)"
        logger.warn(wmsg)
        warnings.warn(wmsg, category=AutoCorrectionWarning)
        return gromacs.mdrun