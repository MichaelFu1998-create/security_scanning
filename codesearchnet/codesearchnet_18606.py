def provider_for_url(self, url):
        """
        Find the right provider for a URL
        """
        for provider, regex in self.get_registry().items():
            if re.match(regex, url) is not None:
                return provider
        
        raise OEmbedMissingEndpoint('No endpoint matches URL: %s' % url)