def _read_certificates(self):
        """
        Reads end-entity and intermediate certificate information from the
        TLS session
        """

        cert_context_pointer_pointer = new(crypt32, 'CERT_CONTEXT **')
        result = secur32.QueryContextAttributesW(
            self._context_handle_pointer,
            Secur32Const.SECPKG_ATTR_REMOTE_CERT_CONTEXT,
            cert_context_pointer_pointer
        )
        handle_error(result, TLSError)

        cert_context_pointer = unwrap(cert_context_pointer_pointer)
        cert_context_pointer = cast(crypt32, 'CERT_CONTEXT *', cert_context_pointer)
        cert_context = unwrap(cert_context_pointer)

        cert_data = bytes_from_buffer(cert_context.pbCertEncoded, native(int, cert_context.cbCertEncoded))
        self._certificate = x509.Certificate.load(cert_data)

        self._intermediates = []

        store_handle = None
        try:
            store_handle = cert_context.hCertStore
            context_pointer = crypt32.CertEnumCertificatesInStore(store_handle, null())
            while not is_null(context_pointer):
                context = unwrap(context_pointer)
                data = bytes_from_buffer(context.pbCertEncoded, native(int, context.cbCertEncoded))
                # The cert store seems to include the end-entity certificate as
                # the last entry, but we already have that from the struct.
                if data != cert_data:
                    self._intermediates.append(x509.Certificate.load(data))
                context_pointer = crypt32.CertEnumCertificatesInStore(store_handle, context_pointer)

        finally:
            if store_handle:
                crypt32.CertCloseStore(store_handle, 0)