def embed(self, url, **kwargs):
        """
        The heart of the matter
        """
        try:
            # first figure out the provider
            provider = self.provider_for_url(url)
        except OEmbedMissingEndpoint:
            raise
        else:
            try:
                # check the database for a cached response, because of certain
                # race conditions that exist with get_or_create(), do a filter
                # lookup and just grab the first item
                stored_match = StoredOEmbed.objects.filter(
                    match=url, 
                    maxwidth=kwargs.get('maxwidth', None), 
                    maxheight=kwargs.get('maxheight', None),
                    date_expires__gte=datetime.datetime.now())[0]
                return OEmbedResource.create_json(stored_match.response_json)
            except IndexError:
                # query the endpoint and cache response in db
                # prevent None from being passed in as a GET param
                params = dict([(k, v) for k, v in kwargs.items() if v])
                
                # request an oembed resource for the url
                resource = provider.request_resource(url, **params)
                
                try:
                    cache_age = int(resource.cache_age)
                    if cache_age < MIN_OEMBED_TTL:
                        cache_age = MIN_OEMBED_TTL
                except:
                    cache_age = DEFAULT_OEMBED_TTL
                
                date_expires = datetime.datetime.now() + datetime.timedelta(seconds=cache_age)
                
                stored_oembed, created = StoredOEmbed.objects.get_or_create(
                    match=url,
                    maxwidth=kwargs.get('maxwidth', None),
                    maxheight=kwargs.get('maxheight', None))
                
                stored_oembed.response_json = resource.json
                stored_oembed.resource_type = resource.type
                stored_oembed.date_expires = date_expires
                
                if resource.content_object:
                    stored_oembed.content_object = resource.content_object
                
                stored_oembed.save()
                return resource