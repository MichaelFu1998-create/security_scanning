def get(self, url, headers=None, params=None):
        """Perform an HTTP GET, using the saved requests.Session and auth info.
        If "Accept" isn't one of the given headers, a default TAXII mime type is
        used.  Regardless, the response type is checked against the accept
        header value, and an exception is raised if they don't match.

        Args:
            url (str): URL to retrieve
            headers (dict): Any other headers to be added to the request.
            params: dictionary or bytes to be sent in the query string for the
                request. (optional)

        """

        merged_headers = self._merge_headers(headers)

        if "Accept" not in merged_headers:
            merged_headers["Accept"] = MEDIA_TYPE_TAXII_V20
        accept = merged_headers["Accept"]

        resp = self.session.get(url, headers=merged_headers, params=params)

        resp.raise_for_status()

        content_type = resp.headers["Content-Type"]

        if not self.valid_content_type(content_type=content_type, accept=accept):
            msg = "Unexpected Response. Got Content-Type: '{}' for Accept: '{}'"
            raise TAXIIServiceException(msg.format(content_type, accept))

        return _to_json(resp)