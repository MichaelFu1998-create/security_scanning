def startlog(filename, overwrite=True):
    """
    @param filename: Start logging on the specified file
    @type filename: string
    @param overwrite: Overwrite or append
        False - Append log to an existing file
        True - Write log to a new file. If file already exist, 
        then erase existing file content and start log
    @type overwrite: boolean

    @return: 1 on success and 0 on error
    @rtype: integer
    """

    if not filename:
        return 0

    if overwrite:
        # Create new file, by overwriting existing file
        _mode = 'w'
    else:
        # Append existing file
        _mode = 'a'
    global _file_logger
    # Create logging file handler
    _file_logger = logging.FileHandler(os.path.expanduser(filename), _mode)
    # Log 'Levelname: Messages', eg: 'ERROR: Logged message'
    _formatter = logging.Formatter('%(levelname)-8s: %(message)s')
    _file_logger.setFormatter(_formatter)
    logger.addHandler(_file_logger)
    if _ldtp_debug:
        # On debug, change the default log level to DEBUG
        _file_logger.setLevel(logging.DEBUG)
    else:
        # else log in case of ERROR level and above
        _file_logger.setLevel(logging.ERROR)

    return 1