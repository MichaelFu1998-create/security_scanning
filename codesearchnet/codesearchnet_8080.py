def storages(self):
        """Iterate over all storages for this projects."""
        stores = self._json(self._get(self._storages_url), 200)
        stores = stores['data']
        for store in stores:
            yield Storage(store, self.session)