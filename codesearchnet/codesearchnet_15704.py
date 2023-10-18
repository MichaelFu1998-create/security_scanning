def refresh_information(self, accept=MEDIA_TYPE_TAXII_V20):
        """Update the properties of this API Root.

        This invokes the ``Get API Root Information`` endpoint.
        """
        response = self.__raw = self._conn.get(self.url,
                                               headers={"Accept": accept})
        self._populate_fields(**response)
        self._loaded_information = True