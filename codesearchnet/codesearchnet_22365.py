def subroute(self, *components):
        """
        See `txspinneret.route.subroute`.

        This decorator can be stacked with itself to specify multiple routes
        with a single handler.
        """
        def _factory(f):
            self._addRoute(f, subroute(*components))
            return f
        return _factory