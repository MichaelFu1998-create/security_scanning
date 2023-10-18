def dispatch(self, request, response):
        """Entry-point of the dispatch cycle for this resource.

        Performs common work such as authentication, decoding, etc. before
        handing complete control of the result to a function with the
        same name as the request method.
        """
        # Assert authentication and attempt to get a valid user object.
        self.require_authentication(request)

        # Assert accessibiltiy of the resource in question.
        self.require_accessibility(request.user, request.method)

        # Facilitate CORS by applying various headers.
        # This must be done on every request.
        # TODO: Provide cross_domain configuration that turns this off.
        self._process_cross_domain_request(request, response)

        # Route the HTTP/1.1 request to an appropriate method.
        return self.route(request, response)