def get_module_logger(moduleName, defaultToVerbose=False):
    """Create a module logger, that can be en/disabled by configuration.

    @see: unit.init_logging
    """
    # moduleName = moduleName.split(".")[-1]
    if not moduleName.startswith(BASE_LOGGER_NAME + "."):
        moduleName = BASE_LOGGER_NAME + "." + moduleName
    logger = logging.getLogger(moduleName)
    # if logger.level == logging.NOTSET and not defaultToVerbose:
    #     logger.setLevel(logging.INFO)  # Disable debug messages by default
    return logger