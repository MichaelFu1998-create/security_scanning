def guid(self, guid):
        """Determines JSONAPI type for provided GUID"""
        return self._json(self._get(self._build_url('guids', guid)), 200)['data']['type']