def safe_joinall(greenlets, timeout=None, raise_error=False):
    """
    Wrapper for gevent.joinall if the greenlet that waits for the joins is killed, it kills all the greenlets it
    joins for.
    """
    greenlets = list(greenlets)
    try:
        gevent.joinall(greenlets, timeout=timeout, raise_error=raise_error)
    except gevent.GreenletExit:
        [greenlet.kill() for greenlet in greenlets if not greenlet.ready()]
        raise
    return greenlets