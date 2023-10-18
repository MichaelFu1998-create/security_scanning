def get_canonical_request(self, req, cano_headers, signed_headers):
        """
        Create the AWS authentication Canonical Request string.

        req            -- Requests PreparedRequest object. Should already
                          include an x-amz-content-sha256 header
        cano_headers   -- Canonical Headers section of Canonical Request, as
                          returned by get_canonical_headers()
        signed_headers -- Signed Headers, as returned by
                          get_canonical_headers()

        """
        url = urlparse(req.url)
        path = self.amz_cano_path(url.path)
        # AWS handles "extreme" querystrings differently to urlparse
        # (see post-vanilla-query-nonunreserved test in aws_testsuite)
        split = req.url.split('?', 1)
        qs = split[1] if len(split) == 2 else ''
        qs = self.amz_cano_querystring(qs)
        payload_hash = req.headers['x-amz-content-sha256']
        req_parts = [req.method.upper(), path, qs, cano_headers,
                     signed_headers, payload_hash]
        cano_req = '\n'.join(req_parts)
        return cano_req