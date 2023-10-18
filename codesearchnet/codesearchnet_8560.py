def get_catalog(self, catalog_id):
        """
        Return specified course catalog.

        Returns:
            dict: catalog details if it is available for the user.

        """
        return self._load_data(
            self.CATALOGS_ENDPOINT,
            default=[],
            resource_id=catalog_id
        )