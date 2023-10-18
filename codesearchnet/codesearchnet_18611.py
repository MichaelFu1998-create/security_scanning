def request_resource(self, url, **kwargs):
        """
        Request an OEmbedResource for a given url.  Some valid keyword args:
        - format
        - maxwidth
        - maxheight
        """
        params = kwargs
        
        params['url'] = url
        params['format'] = 'json'
        
        if '?' in self.endpoint_url:
            url_with_qs = '%s&%s' % (self.endpoint_url.rstrip('&'), urlencode(params))
        else:
            url_with_qs = "%s?%s" % (self.endpoint_url, urlencode(params))
        
        headers, raw_response = self._fetch(url_with_qs)
        resource = self.convert_to_resource(headers, raw_response, params)
        
        return resource