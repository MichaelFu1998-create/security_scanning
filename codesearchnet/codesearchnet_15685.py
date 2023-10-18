def get_sig_string(req, cano_req, scope):
        """
        Generate the AWS4 auth string to sign for the request.

        req      -- Requests PreparedRequest object. This should already
                    include an x-amz-date header.
        cano_req -- The Canonical Request, as returned by
                    get_canonical_request()

        """
        amz_date = req.headers['x-amz-date']
        hsh = hashlib.sha256(cano_req.encode())
        sig_items = ['AWS4-HMAC-SHA256', amz_date, scope, hsh.hexdigest()]
        sig_string = '\n'.join(sig_items)
        return sig_string