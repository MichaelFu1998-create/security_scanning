def _read_certificates(self):
        """
        Reads end-entity and intermediate certificate information from the
        TLS session
        """

        trust_ref = None
        cf_data_ref = None
        result = None

        try:
            trust_ref_pointer = new(Security, 'SecTrustRef *')
            result = Security.SSLCopyPeerTrust(
                self._session_context,
                trust_ref_pointer
            )
            handle_sec_error(result)

            trust_ref = unwrap(trust_ref_pointer)

            number_certs = Security.SecTrustGetCertificateCount(trust_ref)

            self._intermediates = []

            for index in range(0, number_certs):
                sec_certificate_ref = Security.SecTrustGetCertificateAtIndex(
                    trust_ref,
                    index
                )
                cf_data_ref = Security.SecCertificateCopyData(sec_certificate_ref)

                cert_data = CFHelpers.cf_data_to_bytes(cf_data_ref)

                result = CoreFoundation.CFRelease(cf_data_ref)
                handle_cf_error(result)
                cf_data_ref = None

                cert = x509.Certificate.load(cert_data)

                if index == 0:
                    self._certificate = cert
                else:
                    self._intermediates.append(cert)

        finally:
            if trust_ref:
                result = CoreFoundation.CFRelease(trust_ref)
                handle_cf_error(result)
            if cf_data_ref:
                result = CoreFoundation.CFRelease(cf_data_ref)
                handle_cf_error(result)