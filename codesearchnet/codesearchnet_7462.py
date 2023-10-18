def asyncSlot(*args):
    """Make a Qt async slot run on asyncio loop."""
    def outer_decorator(fn):
        @Slot(*args)
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            asyncio.ensure_future(fn(*args, **kwargs))
        return wrapper
    return outer_decorator