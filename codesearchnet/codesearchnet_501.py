def log_if(level, msg, condition, *args):
    """Log 'msg % args' at level 'level' only if condition is fulfilled."""
    if condition:
        vlog(level, msg, *args)