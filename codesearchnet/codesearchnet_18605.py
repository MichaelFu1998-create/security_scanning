def populate(self):
        """
        Populate the internal registry's dictionary with the regexes for each
        provider instance
        """
        self._registry = {}
        
        for provider_class in self._registered_providers:
            instance = provider_class()
            self._registry[instance] = instance.regex
        
        for stored_provider in StoredProvider.objects.active():
            self._registry[stored_provider] = stored_provider.regex
        
        self._populated = True