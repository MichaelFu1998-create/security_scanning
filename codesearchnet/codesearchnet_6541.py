def raw_search(self, query='', params=None):
        """Performs a search query and returns the parsed JSON."""
        if params is None:
            params = {}

        try:
            return self.__index.search(query, params)
        except AlgoliaException as e:
            if DEBUG:
                raise e
            else:
                logger.warning('ERROR DURING SEARCH ON %s: %s', self.index_name, e)