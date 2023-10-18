def init_logs(path=None,
              target=None,
              logger_name='root',
              level=logging.DEBUG,
              maxBytes=1*1024*1024,
              backupCount=5,
              application_name='default',
              server_hostname=None,
              fields=None):
    """Initialize the zlogger.

    Sets up a rotating file handler to the specified path and file with
    the given size and backup count limits, sets the default
    application_name, server_hostname, and default/whitelist fields.

    :param path: path to write the log file
    :param target: name of the log file
    :param logger_name: name of the logger (defaults to root)
    :param level: log level for this logger (defaults to logging.DEBUG)
    :param maxBytes: size of the file before rotation (default 1MB)
    :param application_name: app name to add to each log entry
    :param server_hostname: hostname to add to each log entry
    :param fields: default/whitelist fields.
    :type path: string
    :type target: string
    :type logger_name: string
    :type level: int
    :type maxBytes: int
    :type backupCount: int
    :type application_name: string
    :type server_hostname: string
    :type fields: dict
    """
    log_file = os.path.abspath(
        os.path.join(path, target))
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=maxBytes, backupCount=backupCount)
    handler.setLevel(level)

    handler.setFormatter(
        JsonFormatter(
            application_name=application_name,
            server_hostname=server_hostname,
            fields=fields))

    logger.addHandler(handler)