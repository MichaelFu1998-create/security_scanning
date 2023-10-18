def _forObject(self, obj):
        """
        Create a new `Router` instance, with it's own set of routes, for
        ``obj``.
        """
        router = type(self)()
        router._routes = list(self._routes)
        router._self = obj
        return router