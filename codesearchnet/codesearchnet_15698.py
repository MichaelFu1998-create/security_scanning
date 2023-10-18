def get_objects(self, accept=MEDIA_TYPE_STIX_V20, **filter_kwargs):
        """Implement the ``Get Objects`` endpoint (section 5.3)"""
        self._verify_can_read()
        query_params = _filter_kwargs_to_query_params(filter_kwargs)
        return self._conn.get(self.objects_url, headers={"Accept": accept},
                              params=query_params)