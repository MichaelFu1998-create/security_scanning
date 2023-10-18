def unregister_service(self, name):
        """
        Implementation of :meth:`twitcher.api.IRegistry.unregister_service`.
        """
        try:
            self.store.delete_service(name=name)
        except Exception:
            LOGGER.exception('unregister failed')
            return False
        else:
            return True