def set_gmxrc_environment(gmxrc):
    """Set the environment from ``GMXRC`` provided in *gmxrc*.

    Runs ``GMXRC`` in a subprocess and puts environment variables loaded by it
    into this Python environment.

    If *gmxrc* evaluates to ``False`` then nothing is done. If errors occur
    then only a warning will be logged. Thus, it should be safe to just call
    this function.
    """
    # only v5: 'GMXPREFIX', 'GROMACS_DIR'
    envvars = ['GMXBIN', 'GMXLDLIB', 'GMXMAN', 'GMXDATA',
               'LD_LIBRARY_PATH', 'MANPATH', 'PKG_CONFIG_PATH',
               'PATH',
               'GMXPREFIX', 'GROMACS_DIR']
    # in order to keep empty values, add ___ sentinels around result
    # (will be removed later)
    cmdargs = ['bash', '-c', ". {0} && echo {1}".format(gmxrc,
               ' '.join(['___${{{0}}}___'.format(v) for v in envvars]))]

    if not gmxrc:
        logger.debug("set_gmxrc_environment(): no GMXRC, nothing done.")
        return

    try:
        out = subprocess.check_output(cmdargs)
        out = out.strip().split()
        for key, value in zip(envvars, out):
            value = str(value.decode('ascii').replace('___', ''))  # remove sentinels
            os.environ[key] = value
            logger.debug("set_gmxrc_environment(): %s = %r", key, value)
    except (subprocess.CalledProcessError, OSError):
        logger.warning("Failed to automatically set the Gromacs environment"
                       "from GMXRC=%r", gmxrc)