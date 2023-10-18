def defend_file_methods(coro):
    """
    Decorator. Raises exception when file methods called with wrapped by
    :py:class:`aioftp.AsyncPathIOContext` file object.
    """
    @functools.wraps(coro)
    async def wrapper(self, file, *args, **kwargs):
        if isinstance(file, AsyncPathIOContext):
            raise ValueError("Native path io file methods can not be used "
                             "with wrapped file object")
        return await coro(self, file, *args, **kwargs)
    return wrapper