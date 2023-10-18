def public_key(self):
        """
        :return:
            The PublicKey object for the public key this certificate contains
        """

        if not self._public_key and self.sec_certificate_ref:
            sec_public_key_ref_pointer = new(Security, 'SecKeyRef *')
            res = Security.SecCertificateCopyPublicKey(self.sec_certificate_ref, sec_public_key_ref_pointer)
            handle_sec_error(res)
            sec_public_key_ref = unwrap(sec_public_key_ref_pointer)
            self._public_key = PublicKey(sec_public_key_ref, self.asn1['tbs_certificate']['subject_public_key_info'])

        return self._public_key