def register(self, provider_class):
        """
        Registers a provider with the site.
        """
        if not issubclass(provider_class, BaseProvider):
            raise TypeError('%s is not a subclass of BaseProvider' % provider_class.__name__)
        
        if provider_class in self._registered_providers:
            raise AlreadyRegistered('%s is already registered' % provider_class.__name__)
        
        if issubclass(provider_class, DjangoProvider):
            # set up signal handler for cache invalidation
            signals.post_save.connect(
                self.invalidate_stored_oembeds,
                sender=provider_class._meta.model
            )
        
        # don't build the regex yet - if not all urlconfs have been loaded
        # and processed at this point, the DjangoProvider instances will fail
        # when attempting to reverse urlpatterns that haven't been created.
        # Rather, the regex-list will be populated once, on-demand.
        self._registered_providers.append(provider_class)
        
        # flag for re-population
        self.invalidate_providers()