def link(self, request, response):
        """Processes a `LINK` request.

        A `LINK` request is asking to create a relation from the currently
        represented URI to all of the `Link` request headers.
        """
        from armet.resources.managed.request import read

        if self.slug is None:
            # Mass-LINK is not implemented.
            raise http.exceptions.NotImplemented()

        # Get the current target.
        target = self.read()

        # Collect all the passed link headers.
        links = self._parse_link_headers(request['Link'])

        # Pull targets for each represented link.
        for link in links:
            # Delegate to a connector.
            self.relate(target, read(self, link['uri']))

        # Build the response object.
        self.response.status = http.client.NO_CONTENT
        self.make_response()