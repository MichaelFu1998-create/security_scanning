def get_paginated_catalog_courses(self, catalog_id, querystring=None):
        """
        Return paginated response for all catalog courses.

        Returns:
            dict: API response with links to next and previous pages.

        """
        return self._load_data(
            self.CATALOGS_COURSES_ENDPOINT.format(catalog_id),
            default=[],
            querystring=querystring,
            traverse_pagination=False,
            many=False,
        )