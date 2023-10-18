def with_db_cursor(func):
    """Decorator that supplies a cursor to the function.
    This passes in a psycopg2 Cursor as the argument 'cursor'.
    It also accepts a cursor if one is given.
    """

    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        if 'cursor' in kwargs or func.func_code.co_argcount == len(args):
            return func(*args, **kwargs)
        with db_connect() as db_connection:
            with db_connection.cursor() as cursor:
                kwargs['cursor'] = cursor
                return func(*args, **kwargs)

    return wrapped