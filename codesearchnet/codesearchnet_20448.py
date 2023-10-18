def route(self, request, response):
        """Processes every request.

        Directs control flow to the appropriate HTTP/1.1 method.
        """
        # Ensure that we're allowed to use this HTTP method.
        self.require_http_allowed_method(request)

        # Retrieve the function corresponding to this HTTP method.
        function = getattr(self, request.method.lower(), None)
        if function is None:
            # Server is not capable of supporting it.
            raise http.exceptions.NotImplemented()

        # Delegate to the determined function to process the request.
        return function(request, response)