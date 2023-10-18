def create_log_config(verbose, quiet):
    """
    We use logging's levels as an easy-to-use verbosity controller.
    """
    if verbose and quiet:
        raise ValueError(
            "Supplying both --quiet and --verbose makes no sense."
        )
    elif verbose:
        level = logging.DEBUG
    elif quiet:
        level = logging.ERROR
    else:
        level = logging.INFO

    logger_cfg = {"handlers": ["click_handler"], "level": level}

    return {
        "version": 1,
        "formatters": {"click_formatter": {"format": "%(message)s"}},
        "handlers": {
            "click_handler": {
                "level": level,
                "class": "doc2dash.__main__.ClickEchoHandler",
                "formatter": "click_formatter",
            }
        },
        "loggers": {"doc2dash": logger_cfg, "__main__": logger_cfg},
    }