def autodiscover(self, url):
        """
        Load up StoredProviders from url if it is an oembed scheme
        """
        headers, response = fetch_url(url)
        if headers['content-type'].split(';')[0] in ('application/json', 'text/javascript'):
            provider_data = json.loads(response)
            return self.store_providers(provider_data)