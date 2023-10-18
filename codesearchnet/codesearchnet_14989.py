def get_service_by_name(self, name):
        """
        Implementation of :meth:`twitcher.api.IRegistry.get_service_by_name`.
        """
        try:
            service = self.store.fetch_by_name(name=name)
        except Exception:
            LOGGER.error('Could not get service with name %s', name)
            return {}
        else:
            return service.params