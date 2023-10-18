def refresh(self, accept=MEDIA_TYPE_TAXII_V20):
        """Updates Status information"""
        response = self.__raw = self._conn.get(self.url,
                                               headers={"Accept": accept})
        self._populate_fields(**response)