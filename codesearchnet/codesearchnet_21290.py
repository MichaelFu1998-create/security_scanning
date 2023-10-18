def epoll_poller(timeout=0.0, map=None):
    """
    A poller which uses epoll(), supported on Linux 2.5.44 and newer

    Borrowed from here:
    https://github.com/m13253/python-asyncore-epoll/blob/master/asyncore_epoll.py#L200
    """
    if map is None:
        map = asyncore.socket_map
    pollster = select.epoll()
    if map:
        for fd, obj in iteritems(map):
            flags = 0
            if obj.readable():
                flags |= select.POLLIN | select.POLLPRI
            if obj.writable():
                flags |= select.POLLOUT
            if flags:
                # Only check for exceptions if object was either readable
                # or writable.
                flags |= select.POLLERR | select.POLLHUP | select.POLLNVAL
                pollster.register(fd, flags)
        try:
            r = pollster.poll(timeout)
        except select.error as err:
            if err.args[0] != EINTR:
                raise
            r = []
        for fd, flags in r:
            obj = map.get(fd)
            if obj is None:
                continue
            asyncore.readwrite(obj, flags)