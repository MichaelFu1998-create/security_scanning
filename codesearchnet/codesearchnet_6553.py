def raw_search(self, model, query='', params=None):
        """Performs a search query and returns the parsed JSON."""
        if params is None:
            params = {}

        adapter = self.get_adapter(model)
        return adapter.raw_search(query, params)