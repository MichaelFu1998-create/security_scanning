def do_MKCOL(self, environ, start_response):
        """Handle MKCOL request to create a new collection.

        @see http://www.webdav.org/specs/rfc4918.html#METHOD_MKCOL
        """
        path = environ["PATH_INFO"]
        provider = self._davProvider
        #        res = provider.get_resource_inst(path, environ)

        # Do not understand ANY request body entities
        if util.get_content_length(environ) != 0:
            self._fail(
                HTTP_MEDIATYPE_NOT_SUPPORTED,
                "The server does not handle any body content.",
            )

        # Only accept Depth: 0 (but assume this, if omitted)
        if environ.setdefault("HTTP_DEPTH", "0") != "0":
            self._fail(HTTP_BAD_REQUEST, "Depth must be '0'.")

        if provider.exists(path, environ):
            self._fail(
                HTTP_METHOD_NOT_ALLOWED,
                "MKCOL can only be executed on an unmapped URL.",
            )

        parentRes = provider.get_resource_inst(util.get_uri_parent(path), environ)
        if not parentRes or not parentRes.is_collection:
            self._fail(HTTP_CONFLICT, "Parent must be an existing collection.")

        # TODO: should we check If headers here?
        #        self._evaluate_if_headers(res, environ)
        # Check for write permissions on the PARENT
        self._check_write_permission(parentRes, "0", environ)

        parentRes.create_collection(util.get_uri_name(path))

        return util.send_status_response(environ, start_response, HTTP_CREATED)