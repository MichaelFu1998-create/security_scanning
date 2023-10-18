def compute_digest_response(
        self, realm, user_name, method, uri, nonce, cnonce, qop, nc, environ
    ):
        """Computes digest hash.

        Calculation of the A1 (HA1) part is delegated to the dc interface method
        `digest_auth_user()`.

        Args:
            realm (str):
            user_name (str):
            method (str): WebDAV Request Method
            uri (str):
            nonce (str): server generated nonce value
            cnonce (str): client generated cnonce value
            qop (str): quality of protection
            nc (str) (number), nonce counter incremented by client
        Returns:
            MD5 hash string
            or False if user rejected by domain controller
        """

        def md5h(data):
            return md5(compat.to_bytes(data)).hexdigest()

        def md5kd(secret, data):
            return md5h(secret + ":" + data)

        A1 = self.domain_controller.digest_auth_user(realm, user_name, environ)
        if not A1:
            return False

        A2 = method + ":" + uri

        if qop:
            res = md5kd(
                A1, nonce + ":" + nc + ":" + cnonce + ":" + qop + ":" + md5h(A2)
            )
        else:
            res = md5kd(A1, nonce + ":" + md5h(A2))

        return res