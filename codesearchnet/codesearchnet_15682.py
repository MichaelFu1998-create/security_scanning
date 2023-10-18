def encode_body(req):
        """
        Encode body of request to bytes and update content-type if required.

        If the body of req is Unicode then encode to the charset found in
        content-type header if present, otherwise UTF-8, or ASCII if
        content-type is application/x-www-form-urlencoded. If encoding to UTF-8
        then add charset to content-type. Modifies req directly, does not
        return a modified copy.

        req -- Requests PreparedRequest object

        """
        if isinstance(req.body, text_type):
            split = req.headers.get('content-type', 'text/plain').split(';')
            if len(split) == 2:
                ct, cs = split
                cs = cs.split('=')[1]
                req.body = req.body.encode(cs)
            else:
                ct = split[0]
                if (ct == 'application/x-www-form-urlencoded' or
                        'x-amz-' in ct):
                    req.body = req.body.encode()
                else:
                    req.body = req.body.encode('utf-8')
                    req.headers['content-type'] = ct + '; charset=utf-8'