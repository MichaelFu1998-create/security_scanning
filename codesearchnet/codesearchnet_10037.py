def _read_certificates(self):
        """
        Reads end-entity and intermediate certificate information from the
        TLS session
        """

        stack_pointer = libssl.SSL_get_peer_cert_chain(self._ssl)
        if is_null(stack_pointer):
            handle_openssl_error(0, TLSError)

        if libcrypto_version_info < (1, 1):
            number_certs = libssl.sk_num(stack_pointer)
        else:
            number_certs = libssl.OPENSSL_sk_num(stack_pointer)

        self._intermediates = []

        for index in range(0, number_certs):
            if libcrypto_version_info < (1, 1):
                x509_ = libssl.sk_value(stack_pointer, index)
            else:
                x509_ = libssl.OPENSSL_sk_value(stack_pointer, index)
            buffer_size = libcrypto.i2d_X509(x509_, null())
            cert_buffer = buffer_from_bytes(buffer_size)
            cert_pointer = buffer_pointer(cert_buffer)
            cert_length = libcrypto.i2d_X509(x509_, cert_pointer)
            handle_openssl_error(cert_length)
            cert_data = bytes_from_buffer(cert_buffer, cert_length)

            cert = x509.Certificate.load(cert_data)

            if index == 0:
                self._certificate = cert
            else:
                self._intermediates.append(cert)