def unregister(self, provider_class):
        """
        Unregisters a provider from the site.
        """
        if not issubclass(provider_class, BaseProvider):
            raise TypeError('%s must be a subclass of BaseProvider' % provider_class.__name__)
        
        if provider_class not in self._registered_providers:
            raise NotRegistered('%s is not registered' % provider_class.__name__)
        
        self._registered_providers.remove(provider_class)
        
        # flag for repopulation
        self.invalidate_providers()