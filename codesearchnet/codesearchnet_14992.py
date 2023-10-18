def clear_services(self):
        """
        Implementation of :meth:`twitcher.api.IRegistry.clear_services`.
        """
        try:
            self.store.clear_services()
        except Exception:
            LOGGER.error('Clear services failed.')
            return False
        else:
            return True