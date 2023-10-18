def log_callback(wrapped_function):
    """Decorator that produces DEBUG level log messages before and after
    calling a parser method.

    If a callback raises an IgnoredMatchException the log will show 'IGNORED'
    instead to indicate that the parser will not create any objects from
    the matched string.

    Example:
        DEBUG:poyo.parser:parse_simple <-     123: 456.789
        DEBUG:poyo.parser:parse_int <- 123
        DEBUG:poyo.parser:parse_int -> 123
        DEBUG:poyo.parser:parse_float <- 456.789
        DEBUG:poyo.parser:parse_float -> 456.789
        DEBUG:poyo.parser:parse_simple -> <Simple name: 123, value: 456.789>
    """

    def debug_log(message):
        """Helper to log an escaped version of the given message to DEBUG"""
        logger.debug(message.encode('unicode_escape').decode())

    @functools.wraps(wrapped_function)
    def _wrapper(parser, match, **kwargs):
        func_name = wrapped_function.__name__

        debug_log(u'{func_name} <- {matched_string}'.format(
            func_name=func_name,
            matched_string=match.group(),
        ))

        try:
            result = wrapped_function(parser, match, **kwargs)
        except IgnoredMatchException:
            debug_log(u'{func_name} -> IGNORED'.format(func_name=func_name))
            raise

        debug_log(u'{func_name} -> {result}'.format(
            func_name=func_name,
            result=result,
        ))

        return result
    return _wrapper