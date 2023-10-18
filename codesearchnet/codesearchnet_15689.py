def sign_sha256(key, msg):
        """
        Generate an SHA256 HMAC, encoding msg to UTF-8 if not
        already encoded.

        key -- signing key. bytes.
        msg -- message to sign. unicode or bytes.

        """
        if isinstance(msg, text_type):
            msg = msg.encode('utf-8')
        return hmac.new(key, msg, hashlib.sha256).digest()