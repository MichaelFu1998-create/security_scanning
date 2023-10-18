def get_server(self, key, **kwds):
        """
        Get a new or existing server for this key.

        :param int key: key for the server to use
        """
        kwds = dict(self.kwds, **kwds)
        server = self.servers.get(key)
        if server:
            # Make sure it's the right server.
            server.check_keywords(self.constructor, kwds)
        else:
            # Make a new server
            server = _CachedServer(self.constructor, key, kwds)
            self.servers[key] = server

        return server