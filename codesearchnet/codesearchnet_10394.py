def stop_logging():
    """Stop logging to logfile and console."""
    from . import log
    logger = logging.getLogger("gromacs")
    logger.info("GromacsWrapper %s STOPPED logging", get_version())
    log.clear_handlers(logger)