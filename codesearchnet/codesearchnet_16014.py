def validateRequest(self, uri, postVars, expectedSignature):
        """validate a request from plivo

        uri: the full URI that Plivo requested on your server
        postVars: post vars that Plivo sent with the request
        expectedSignature: signature in HTTP X-Plivo-Signature header

        returns true if the request passes validation, false if not
        """

        # append the POST variables sorted by key to the uri
        s = uri
        for k, v in sorted(postVars.items()):
            s += k + v

        # compute signature and compare signatures
        return (base64.encodestring(hmac.new(self.auth_token, s, sha1).digest()).\
            strip() == expectedSignature)