def get_object(self, obj_id, version=None, accept=MEDIA_TYPE_STIX_V20):
        """Implement the ``Get an Object`` endpoint (section 5.5)"""
        self._verify_can_read()
        url = self.objects_url + str(obj_id) + "/"
        query_params = None
        if version:
            query_params = _filter_kwargs_to_query_params({"version": version})
        return self._conn.get(url, headers={"Accept": accept},
                              params=query_params)