def _addRoute(self, f, matcher):
        """
        Add a route handler and matcher to the collection of possible routes.
        """
        self._routes.append((f.func_name, f, matcher))