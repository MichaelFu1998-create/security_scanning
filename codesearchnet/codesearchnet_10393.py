def start_logging(logfile="gromacs.log"):
    """Start logging of messages to file and console.

    The default logfile is named ``gromacs.log`` and messages are
    logged with the tag *gromacs*.
    """
    from . import log
    log.create("gromacs", logfile=logfile)
    logging.getLogger("gromacs").info("GromacsWrapper %s STARTED logging to %r",
                                      __version__, logfile)