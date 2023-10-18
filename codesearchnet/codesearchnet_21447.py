def transaction(func):
    """
    Provides a transacted cursor which will run in autocommit=false mode

    For any exception the transaction will be rolled back.
    Requires that the function being decorated is an instance of a class or object
    that yields a cursor from a get_cursor(cursor_type=CursorType.NAMEDTUPLE) coroutine or provides such an object
    as the first argument in its signature

    Yields:
        A client-side transacted named cursor
    """

    @wraps(func)
    def wrapper(cls, *args, **kwargs):
        with (yield from cls.get_cursor(_CursorType.NAMEDTUPLE)) as c:
            try:
                yield from c.execute('BEGIN')
                result = (yield from func(cls, c, *args, **kwargs))
            except Exception:
                yield from c.execute('ROLLBACK')
            else:
                yield from c.execute('COMMIT')
                return result

    return wrapper