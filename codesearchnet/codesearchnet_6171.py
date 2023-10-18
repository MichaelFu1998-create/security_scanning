def init_logging(config):
    """Initialize base logger named 'wsgidav'.

    The base logger is filtered by the `verbose` configuration option.
    Log entries will have a time stamp and thread id.

    :Parameters:
        verbose : int
            Verbosity configuration (0..5)
        enable_loggers : string list
            List of module logger names, that will be switched to DEBUG level.

    Module loggers
    ~~~~~~~~~~~~~~
    Module loggers (e.g 'wsgidav.lock_manager') are named loggers, that can be
    independently switched to DEBUG mode.

    Except for verbosity, they will inherit settings from the base logger.

    They will suppress DEBUG level messages, unless they are enabled by passing
    their name to util.init_logging().

    If enabled, module loggers will print DEBUG messages, even if verbose == 3.

    Example initialize and use a module logger, that will generate output,
    if enabled (and verbose >= 2)::

        _logger = util.get_module_logger(__name__)
        [..]
        _logger.debug("foo: '{}'".format(s))

    This logger would be enabled by passing its name to init_logging()::

        enable_loggers = ["lock_manager",
                          "property_manager",
                         ]
        util.init_logging(2, enable_loggers)


    Log Level Matrix
    ~~~~~~~~~~~~~~~~

    +---------+--------+---------------------------------------------------------------+
    | Verbose | Option |                       Log level                               |
    | level   |        +-------------+------------------------+------------------------+
    |         |        | base logger | module logger(default) | module logger(enabled) |
    +=========+========+=============+========================+========================+
    |    0    | -qqq   | CRITICAL    | CRITICAL               | CRITICAL               |
    +---------+--------+-------------+------------------------+------------------------+
    |    1    | -qq    | ERROR       | ERROR                  | ERROR                  |
    +---------+--------+-------------+------------------------+------------------------+
    |    2    | -q     | WARN        | WARN                   | WARN                   |
    +---------+--------+-------------+------------------------+------------------------+
    |    3    |        | INFO        | INFO                   | **DEBUG**              |
    +---------+--------+-------------+------------------------+------------------------+
    |    4    | -v     | DEBUG       | DEBUG                  | DEBUG                  |
    +---------+--------+-------------+------------------------+------------------------+
    |    5    | -vv    | DEBUG       | DEBUG                  | DEBUG                  |
    +---------+--------+-------------+------------------------+------------------------+

    """
    verbose = config.get("verbose", 3)

    enable_loggers = config.get("enable_loggers", [])
    if enable_loggers is None:
        enable_loggers = []

    logger_date_format = config.get("logger_date_format", "%Y-%m-%d %H:%M:%S")
    logger_format = config.get(
        "logger_format",
        "%(asctime)s.%(msecs)03d - <%(thread)d> %(name)-27s %(levelname)-8s:  %(message)s",
    )

    formatter = logging.Formatter(logger_format, logger_date_format)

    # Define handlers
    consoleHandler = logging.StreamHandler(sys.stdout)
    #    consoleHandler = logging.StreamHandler(sys.stderr)
    consoleHandler.setFormatter(formatter)
    # consoleHandler.setLevel(logging.DEBUG)

    # Add the handlers to the base logger
    logger = logging.getLogger(BASE_LOGGER_NAME)

    if verbose >= 4:  # --verbose
        logger.setLevel(logging.DEBUG)
    elif verbose == 3:  # default
        logger.setLevel(logging.INFO)
    elif verbose == 2:  # --quiet
        logger.setLevel(logging.WARN)
        # consoleHandler.setLevel(logging.WARN)
    elif verbose == 1:  # -qq
        logger.setLevel(logging.ERROR)
        # consoleHandler.setLevel(logging.WARN)
    else:  # -qqq
        logger.setLevel(logging.CRITICAL)
        # consoleHandler.setLevel(logging.ERROR)

    # Don't call the root's handlers after our custom handlers
    logger.propagate = False

    # Remove previous handlers
    for hdlr in logger.handlers[:]:  # Must iterate an array copy
        try:
            hdlr.flush()
            hdlr.close()
        except Exception:
            pass
        logger.removeHandler(hdlr)

    logger.addHandler(consoleHandler)

    if verbose >= 3:
        for e in enable_loggers:
            if not e.startswith(BASE_LOGGER_NAME + "."):
                e = BASE_LOGGER_NAME + "." + e
            lg = logging.getLogger(e.strip())
            lg.setLevel(logging.DEBUG)