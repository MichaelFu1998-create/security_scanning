def list_services(self):
        """
        Implementation of :meth:`twitcher.api.IRegistry.list_services`.
        """
        try:
            services = [service.params for service in self.store.list_services()]
        except Exception:
            LOGGER.error('List services failed.')
            return []
        else:
            return services