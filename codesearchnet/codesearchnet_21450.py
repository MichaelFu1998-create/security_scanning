def get_cursor(cls, cursor_type=_CursorType.PLAIN) -> Cursor:
        """
        Yields:
            new client-side cursor from existing db connection pool
        """
        _cur = None
        if cls._use_pool:
            _connection_source = yield from cls.get_pool()
        else:
            _connection_source = yield from aiopg.connect(echo=False, **cls._connection_params)

        if cursor_type == _CursorType.PLAIN:
            _cur = yield from _connection_source.cursor()
        if cursor_type == _CursorType.NAMEDTUPLE:
            _cur = yield from _connection_source.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)
        if cursor_type == _CursorType.DICT:
            _cur = yield from _connection_source.cursor(cursor_factory=psycopg2.extras.DictCursor)

        if not cls._use_pool:
            _cur = cursor_context_manager(_connection_source, _cur)

        return _cur