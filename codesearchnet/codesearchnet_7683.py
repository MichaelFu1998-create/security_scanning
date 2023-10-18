def backends(cls):
        """
        Discover all keyrings for chaining.
        """
        allowed = (
            keyring
            for keyring in filter(backend._limit, backend.get_all_keyring())
            if not isinstance(keyring, ChainerBackend)
            and keyring.priority > 0
        )
        return sorted(allowed, key=backend.by_priority, reverse=True)