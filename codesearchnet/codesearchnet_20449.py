def options(self, request, response):
        """Process an `OPTIONS` request.

        Used to initiate a cross-origin request. All handling specific to
        CORS requests is done on every request however this method also
        returns a list of available methods.
        """
        # Gather a list available HTTP/1.1 methods for this URI.
        response['Allowed'] = ', '.join(self.meta.http_allowed_methods)

        # All CORS handling is done for every HTTP/1.1 method.
        # No more handling is neccesary; set the response to 200 and return.
        response.status = http.client.OK