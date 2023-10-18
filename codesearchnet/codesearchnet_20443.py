def _process_cross_domain_request(cls, request, response):
        """Facilitate Cross-Origin Requests (CORs).
        """

        # Step 1
        # Check for Origin header.
        origin = request.get('Origin')
        if not origin:
            return

        # Step 2
        # Check if the origin is in the list of allowed origins.
        if not (origin in cls.meta.http_allowed_origins or
                '*' == cls.meta.http_allowed_origins):
            return

        # Step 3
        # Try to parse the Request-Method header if it exists.
        method = request.get('Access-Control-Request-Method')
        if method and method not in cls.meta.http_allowed_methods:
            return

        # Step 4
        # Try to parse the Request-Header header if it exists.
        headers = request.get('Access-Control-Request-Headers', ())
        if headers:
            headers = [h.strip() for h in headers.split(',')]

        # Step 5
        # Check if the headers are allowed on this resource.
        allowed_headers = [h.lower() for h in cls.meta.http_allowed_headers]
        if any(h.lower() not in allowed_headers for h in headers):
            return

        # Step 6
        # Always add the origin.
        response['Access-Control-Allow-Origin'] = origin

        # TODO: Check if we can provide credentials.
        response['Access-Control-Allow-Credentials'] = 'true'

        # Step 7
        # TODO: Optionally add Max-Age header.

        # Step 8
        # Add the allowed methods.
        allowed_methods = ', '.join(cls.meta.http_allowed_methods)
        response['Access-Control-Allow-Methods'] = allowed_methods

        # Step 9
        # Add any allowed headers.
        allowed_headers = ', '.join(cls.meta.http_allowed_headers)
        if allowed_headers:
            response['Access-Control-Allow-Headers'] = allowed_headers

        # Step 10
        # Add any exposed headers.
        exposed_headers = ', '.join(cls.meta.http_exposed_headers)
        if exposed_headers:
            response['Access-Control-Expose-Headers'] = exposed_headers