def fetch_by_name(self, name):
        """
        Get service for given ``name`` from memory storage.
        """
        service = self.name_index.get(name)
        if not service:
            raise ServiceNotFound
        return Service(service)