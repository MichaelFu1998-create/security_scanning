def get_manifest(self, accept=MEDIA_TYPE_TAXII_V20, **filter_kwargs):
        """Implement the ``Get Object Manifests`` endpoint (section 5.6)."""
        self._verify_can_read()
        query_params = _filter_kwargs_to_query_params(filter_kwargs)
        return self._conn.get(self.url + "manifest/",
                              headers={"Accept": accept},
                              params=query_params)