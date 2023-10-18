def universal_exception(coro):
    """
    Decorator. Reraising any exception (except `CancelledError` and
    `NotImplementedError`) with universal exception
    :py:class:`aioftp.PathIOError`
    """
    @functools.wraps(coro)
    async def wrapper(*args, **kwargs):
        try:
            return await coro(*args, **kwargs)
        except (asyncio.CancelledError, NotImplementedError,
                StopAsyncIteration):
            raise
        except Exception:
            raise errors.PathIOError(reason=sys.exc_info())

    return wrapper