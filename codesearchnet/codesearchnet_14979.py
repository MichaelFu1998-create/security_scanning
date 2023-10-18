def fetch_by_url(self, url):
        """
        Gets service for given ``url`` from mongodb storage.
        """
        service = self.collection.find_one({'url': url})
        if not service:
            raise ServiceNotFound
        return Service(service)