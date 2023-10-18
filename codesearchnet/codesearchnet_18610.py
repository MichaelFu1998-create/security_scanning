def store_providers(self, provider_data):
        """
        Iterate over the returned json and try to sort out any new providers
        """
        if not hasattr(provider_data, '__iter__'):
            raise OEmbedException('Autodiscovered response not iterable')
        
        provider_pks = []
        
        for provider in provider_data:
            if 'endpoint' not in provider or \
               'matches' not in provider:
                continue
            
            resource_type = provider.get('type')
            if resource_type not in RESOURCE_TYPES:
                continue
            
            stored_provider, created = StoredProvider.objects.get_or_create(
                wildcard_regex=provider['matches']
            )
            
            if created:
                stored_provider.endpoint_url = relative_to_full(    
                    provider['endpoint'],
                    provider['matches']
                )
                stored_provider.resource_type = resource_type
                stored_provider.save()
            
            provider_pks.append(stored_provider.pk)
        
        return StoredProvider.objects.filter(pk__in=provider_pks)