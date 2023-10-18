def get_paginated_catalogs(self, querystring=None):
        """
        Return a paginated list of course catalogs, including name and ID.

        Returns:
            dict: Paginated response containing catalogs available for the user.

        """
        return self._load_data(
            self.CATALOGS_ENDPOINT,
            default=[],
            querystring=querystring,
            traverse_pagination=False,
            many=False
        )