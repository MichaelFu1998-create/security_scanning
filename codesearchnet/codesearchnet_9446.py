def worker(f):
    """
    Decorator. Abortable worker. If wrapped task will be cancelled by
    dispatcher, decorator will send ftp codes of successful interrupt.

    ::

        >>> @worker
        ... async def worker(self, connection, rest):
        ...     ...

    """
    @functools.wraps(f)
    async def wrapper(cls, connection, rest):
        try:
            await f(cls, connection, rest)
        except asyncio.CancelledError:
            connection.response("426", "transfer aborted")
            connection.response("226", "abort successful")

    return wrapper