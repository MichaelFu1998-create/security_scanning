def init_logging(name, level=logging.INFO):
    """Logging config

    Set the level and create a more detailed formatter for debug mode.

    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    try:
        if os.isatty(sys.stdout.fileno()) and \
                not sys.platform.startswith('win'):
            formatter = ColoredFormatter()
        elif level == logging.DEBUG:
            formatter = Formatter('%(levelname)s - %(message)s')
        else:
            formatter = Formatter('%(message)s')
    except Exception:
        # This fails when running tests with click (test_build)
        formatter = Formatter('%(message)s')

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)