def route(self, *components):
        """
        See `txspinneret.route.route`.

        This decorator can be stacked with itself to specify multiple routes
        with a single handler.
        """
        def _factory(f):
            self._addRoute(f, route(*components))
            return f
        return _factory