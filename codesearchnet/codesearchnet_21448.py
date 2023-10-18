def connect(cls, database: str, user: str, password: str, host: str, port: int, *, use_pool: bool=True,
                enable_ssl: bool=False, minsize=1, maxsize=50, keepalives_idle=5, keepalives_interval=4, echo=False,
                **kwargs):
        """
        Sets connection parameters
        For more information on the parameters that is accepts,
        see : http://www.postgresql.org/docs/9.2/static/libpq-connect.html
        """
        cls._connection_params['database'] = database
        cls._connection_params['user'] = user
        cls._connection_params['password'] = password
        cls._connection_params['host'] = host
        cls._connection_params['port'] = port
        cls._connection_params['sslmode'] = 'prefer' if enable_ssl else 'disable'
        cls._connection_params['minsize'] = minsize
        cls._connection_params['maxsize'] = maxsize
        cls._connection_params['keepalives_idle'] = keepalives_idle
        cls._connection_params['keepalives_interval'] = keepalives_interval
        cls._connection_params['echo'] = echo
        cls._connection_params.update(kwargs)
        cls._use_pool = use_pool