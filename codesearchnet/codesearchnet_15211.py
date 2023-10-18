def _get_connection(cls, connection: Optional[str] = None) -> str:
        """Get a default connection string.

        Wraps :func:`bio2bel.utils.get_connection` and passing this class's :data:`module_name` to it.
        """
        return get_connection(cls.module_name, connection=connection)