def _totals(self, query):
        """ General method for returning total counts
        """
        self.add_parameters(limit=1)
        query = self._build_query(query)
        self._retrieve_data(query)
        self.url_params = None
        # extract the 'total items' figure
        return int(self.request.headers["Total-Results"])