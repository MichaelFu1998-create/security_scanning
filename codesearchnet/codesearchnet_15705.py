def refresh_collections(self, accept=MEDIA_TYPE_TAXII_V20):
        """Update the list of Collections contained by this API Root.

        This invokes the ``Get Collections`` endpoint.
        """
        url = self.url + "collections/"
        response = self._conn.get(url, headers={"Accept": accept})

        self._collections = []
        for item in response.get("collections", []):  # optional
            collection_url = url + item["id"] + "/"
            collection = Collection(collection_url, conn=self._conn,
                                    collection_info=item)
            self._collections.append(collection)

        self._loaded_collections = True