def log_every_n(level, msg, n, *args):
    """Log 'msg % args' at level 'level' once per 'n' times.

    Logs the 1st call, (N+1)st call, (2N+1)st call,  etc.
    Not threadsafe.

    Args:
    level: The level at which to log.
    msg: The message to be logged.
    n: The number of times this should be called before it is logged.
    *args: The args to be substituted into the msg.
    """
    count = _GetNextLogCountPerToken(_GetFileAndLine())
    log_if(level, msg, not (count % n), *args)