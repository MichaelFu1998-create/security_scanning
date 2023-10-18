def get_canonical_headers(cls, req, include=None):
        """
        Generate the Canonical Headers section of the Canonical Request.

        Return the Canonical Headers and the Signed Headers strs as a tuple
        (canonical_headers, signed_headers).

        req     -- Requests PreparedRequest object
        include -- List of headers to include in the canonical and signed
                   headers. It's primarily included to allow testing against
                   specific examples from Amazon. If omitted or None it
                   includes host, content-type and any header starting 'x-amz-'
                   except for x-amz-client context, which appears to break
                   mobile analytics auth if included. Except for the
                   x-amz-client-context exclusion these defaults are per the
                   AWS documentation.

        """
        if include is None:
            include = cls.default_include_headers
        include = [x.lower() for x in include]
        headers = req.headers.copy()
        # Temporarily include the host header - AWS requires it to be included
        # in the signed headers, but Requests doesn't include it in a
        # PreparedRequest
        if 'host' not in headers:
            headers['host'] = urlparse(req.url).netloc.split(':')[0]
        # Aggregate for upper/lowercase header name collisions in header names,
        # AMZ requires values of colliding headers be concatenated into a
        # single header with lowercase name.  Although this is not possible with
        # Requests, since it uses a case-insensitive dict to hold headers, this
        # is here just in case you duck type with a regular dict
        cano_headers_dict = {}
        for hdr, val in headers.items():
            hdr = hdr.strip().lower()
            val = cls.amz_norm_whitespace(val).strip()
            if (hdr in include or '*' in include or
                    ('x-amz-*' in include and hdr.startswith('x-amz-') and not
                    hdr == 'x-amz-client-context')):
                vals = cano_headers_dict.setdefault(hdr, [])
                vals.append(val)
        # Flatten cano_headers dict to string and generate signed_headers
        cano_headers = ''
        signed_headers_list = []
        for hdr in sorted(cano_headers_dict):
            vals = cano_headers_dict[hdr]
            val = ','.join(sorted(vals))
            cano_headers += '{}:{}\n'.format(hdr, val)
            signed_headers_list.append(hdr)
        signed_headers = ';'.join(signed_headers_list)
        return (cano_headers, signed_headers)