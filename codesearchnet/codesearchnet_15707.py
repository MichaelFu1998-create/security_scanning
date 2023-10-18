def refresh(self):
        """Update the Server information and list of API Roots"""
        response = self.__raw = self._conn.get(self.url)
        self._populate_fields(**response)
        self._loaded = True