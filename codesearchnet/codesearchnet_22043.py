def spawn(func, *args, **kwargs):
    """ spawns a greenlet that does not print exceptions to the screen.
    if you use this function you MUST use this module's join or joinall otherwise the exception will be lost """
    return gevent.spawn(wrap_uncaught_greenlet_exceptions(func), *args, **kwargs)