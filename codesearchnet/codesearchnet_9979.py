def public_key(self):
        """
        :return:
            The PublicKey object for the public key this certificate contains
        """

        if not self._public_key and self.x509:
            evp_pkey = libcrypto.X509_get_pubkey(self.x509)
            self._public_key = PublicKey(evp_pkey, self.asn1['tbs_certificate']['subject_public_key_info'])

        return self._public_key