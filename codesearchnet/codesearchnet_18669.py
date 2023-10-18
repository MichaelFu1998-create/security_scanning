def inject_quiet(levels):
    """see --quiet flag help for what this does"""
    loggers = list(Logger.manager.loggerDict.items())
    loggers.append(("root", getLogger()))
    level_filter = LevelFilter(levels)

    for logger_name, logger in loggers:
        for handler in getattr(logger, "handlers", []):
            handler.addFilter(level_filter)