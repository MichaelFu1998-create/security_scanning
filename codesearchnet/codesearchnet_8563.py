def get_catalog_courses(self, catalog_id):
        """
        Return the courses included in a single course catalog by ID.

        Args:
            catalog_id (int): The catalog ID we want to retrieve.

        Returns:
            list: Courses of the catalog in question

        """
        return self._load_data(
            self.CATALOGS_COURSES_ENDPOINT.format(catalog_id),
            default=[]
        )