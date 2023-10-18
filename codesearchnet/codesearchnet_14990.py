def get_service_by_url(self, url):
        """
        Implementation of :meth:`twitcher.api.IRegistry.get_service_by_url`.
        """
        try:
            service = self.store.fetch_by_url(url=url)
        except Exception:
            LOGGER.error('Could not get service with url %s', url)
            return {}
        else:
            return service.params