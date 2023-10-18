def build_twisted_request(self, method, url, extra_headers={}, body_producer=None, full_url=False):
        """ Build a request for twisted

        Args:
            method (str): Request method (GET/POST/PUT/DELETE/etc.) If not specified, it will be POST if post_data is not None
            url (str): Destination URL (full, or relative)

        Kwargs:
            extra_headers (dict): Headers (override default connection headers, if any)
            body_producer (:class:`twisted.web.iweb.IBodyProducer`): Object producing request body
            full_url (bool): If False, URL is relative

        Returns:
            tuple. Tuple with two elements: reactor, and request
        """
        uri = url if full_url else self._url(url)

        raw_headers = self.get_headers()
        if extra_headers:
            raw_headers.update(extra_headers)

        headers = http_headers.Headers()
        for header in raw_headers:
            headers.addRawHeader(header, raw_headers[header])

        agent = client.Agent(reactor)
        request = agent.request(method, uri, headers, body_producer)

        return (reactor, request)