def require_http_allowed_method(cls, request):
        """Ensure that we're allowed to use this HTTP method."""
        allowed = cls.meta.http_allowed_methods
        if request.method not in allowed:
            # The specified method is not allowed for the resource
            # identified by the request URI.
            # RFC 2616 § 10.4.6 — 405 Method Not Allowed
            raise http.exceptions.MethodNotAllowed(allowed)