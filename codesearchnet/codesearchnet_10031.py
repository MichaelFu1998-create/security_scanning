def _handshake(self):
        """
        Perform an initial TLS handshake
        """

        self._ssl = None
        self._rbio = None
        self._wbio = None

        try:
            self._ssl = libssl.SSL_new(self._session._ssl_ctx)
            if is_null(self._ssl):
                self._ssl = None
                handle_openssl_error(0)

            mem_bio = libssl.BIO_s_mem()

            self._rbio = libssl.BIO_new(mem_bio)
            if is_null(self._rbio):
                handle_openssl_error(0)

            self._wbio = libssl.BIO_new(mem_bio)
            if is_null(self._wbio):
                handle_openssl_error(0)

            libssl.SSL_set_bio(self._ssl, self._rbio, self._wbio)

            utf8_domain = self._hostname.encode('utf-8')
            libssl.SSL_ctrl(
                self._ssl,
                LibsslConst.SSL_CTRL_SET_TLSEXT_HOSTNAME,
                LibsslConst.TLSEXT_NAMETYPE_host_name,
                utf8_domain
            )

            libssl.SSL_set_connect_state(self._ssl)

            if self._session._ssl_session:
                libssl.SSL_set_session(self._ssl, self._session._ssl_session)

            self._bio_write_buffer = buffer_from_bytes(self._buffer_size)
            self._read_buffer = buffer_from_bytes(self._buffer_size)

            handshake_server_bytes = b''
            handshake_client_bytes = b''

            while True:
                result = libssl.SSL_do_handshake(self._ssl)
                handshake_client_bytes += self._raw_write()

                if result == 1:
                    break

                error = libssl.SSL_get_error(self._ssl, result)
                if error == LibsslConst.SSL_ERROR_WANT_READ:
                    chunk = self._raw_read()
                    if chunk == b'':
                        if handshake_server_bytes == b'':
                            raise_disconnection()
                        if detect_client_auth_request(handshake_server_bytes):
                            raise_client_auth()
                        raise_protocol_error(handshake_server_bytes)
                    handshake_server_bytes += chunk

                elif error == LibsslConst.SSL_ERROR_WANT_WRITE:
                    handshake_client_bytes += self._raw_write()

                elif error == LibsslConst.SSL_ERROR_ZERO_RETURN:
                    self._gracefully_closed = True
                    self._shutdown(False)
                    self._raise_closed()

                else:
                    info = peek_openssl_error()

                    if libcrypto_version_info < (1, 1):
                        dh_key_info = (
                            20,
                            LibsslConst.SSL_F_SSL3_CHECK_CERT_AND_ALGORITHM,
                            LibsslConst.SSL_R_DH_KEY_TOO_SMALL
                        )
                    else:
                        dh_key_info = (
                            20,
                            LibsslConst.SSL_F_TLS_PROCESS_SKE_DHE,
                            LibsslConst.SSL_R_DH_KEY_TOO_SMALL
                        )
                    if info == dh_key_info:
                        raise_dh_params()

                    if libcrypto_version_info < (1, 1):
                        unknown_protocol_info = (
                            20,
                            LibsslConst.SSL_F_SSL23_GET_SERVER_HELLO,
                            LibsslConst.SSL_R_UNKNOWN_PROTOCOL
                        )
                    else:
                        unknown_protocol_info = (
                            20,
                            LibsslConst.SSL_F_SSL3_GET_RECORD,
                            LibsslConst.SSL_R_WRONG_VERSION_NUMBER
                        )
                    if info == unknown_protocol_info:
                        raise_protocol_error(handshake_server_bytes)

                    tls_version_info_error = (
                        20,
                        LibsslConst.SSL_F_SSL23_GET_SERVER_HELLO,
                        LibsslConst.SSL_R_TLSV1_ALERT_PROTOCOL_VERSION
                    )
                    if info == tls_version_info_error:
                        raise_protocol_version()

                    handshake_error_info = (
                        20,
                        LibsslConst.SSL_F_SSL23_GET_SERVER_HELLO,
                        LibsslConst.SSL_R_SSLV3_ALERT_HANDSHAKE_FAILURE
                    )
                    if info == handshake_error_info:
                        raise_handshake()

                    handshake_failure_info = (
                        20,
                        LibsslConst.SSL_F_SSL3_READ_BYTES,
                        LibsslConst.SSL_R_SSLV3_ALERT_HANDSHAKE_FAILURE
                    )
                    if info == handshake_failure_info:
                        raise_client_auth()

                    if libcrypto_version_info < (1, 1):
                        cert_verify_failed_info = (
                            20,
                            LibsslConst.SSL_F_SSL3_GET_SERVER_CERTIFICATE,
                            LibsslConst.SSL_R_CERTIFICATE_VERIFY_FAILED
                        )
                    else:
                        cert_verify_failed_info = (
                            20,
                            LibsslConst.SSL_F_TLS_PROCESS_SERVER_CERTIFICATE,
                            LibsslConst.SSL_R_CERTIFICATE_VERIFY_FAILED
                        )

                    if info == cert_verify_failed_info:
                        verify_result = libssl.SSL_get_verify_result(self._ssl)
                        chain = extract_chain(handshake_server_bytes)

                        self_signed = False
                        time_invalid = False
                        no_issuer = False
                        cert = None
                        oscrypto_cert = None

                        if chain:
                            cert = chain[0]
                            oscrypto_cert = load_certificate(cert)
                            self_signed = oscrypto_cert.self_signed

                            issuer_error_codes = set([
                                LibsslConst.X509_V_ERR_DEPTH_ZERO_SELF_SIGNED_CERT,
                                LibsslConst.X509_V_ERR_SELF_SIGNED_CERT_IN_CHAIN,
                                LibsslConst.X509_V_ERR_UNABLE_TO_GET_ISSUER_CERT_LOCALLY
                            ])
                            if verify_result in issuer_error_codes:
                                no_issuer = not self_signed

                            time_error_codes = set([
                                LibsslConst.X509_V_ERR_CERT_HAS_EXPIRED,
                                LibsslConst.X509_V_ERR_CERT_NOT_YET_VALID
                            ])
                            time_invalid = verify_result in time_error_codes

                        if time_invalid:
                            raise_expired_not_yet_valid(cert)
                        if no_issuer:
                            raise_no_issuer(cert)
                        if self_signed:
                            raise_self_signed(cert)
                        if oscrypto_cert and oscrypto_cert.asn1.hash_algo in set(['md5', 'md2']):
                            raise_weak_signature(oscrypto_cert)
                        raise_verification(cert)

                    handle_openssl_error(0, TLSError)

            session_info = parse_session_info(
                handshake_server_bytes,
                handshake_client_bytes
            )
            self._protocol = session_info['protocol']
            self._cipher_suite = session_info['cipher_suite']
            self._compression = session_info['compression']
            self._session_id = session_info['session_id']
            self._session_ticket = session_info['session_ticket']

            if self._cipher_suite.find('_DHE_') != -1:
                dh_params_length = get_dh_params_length(handshake_server_bytes)
                if dh_params_length < 1024:
                    self.close()
                    raise_dh_params()

            # When saving the session for future requests, we use
            # SSL_get1_session() variant to increase the reference count. This
            # prevents the session from being freed when one connection closes
            # before another is opened. However, since we increase the ref
            # count, we also have to explicitly free any previous session.
            if self._session_id == 'new' or self._session_ticket == 'new':
                if self._session._ssl_session:
                    libssl.SSL_SESSION_free(self._session._ssl_session)
                self._session._ssl_session = libssl.SSL_get1_session(self._ssl)

            if not self._session._manual_validation:
                if self.certificate.hash_algo in set(['md5', 'md2']):
                    raise_weak_signature(self.certificate)

                # OpenSSL does not do hostname or IP address checking in the end
                # entity certificate, so we must perform that check
                if not self.certificate.is_valid_domain_ip(self._hostname):
                    raise_hostname(self.certificate, self._hostname)

        except (OSError, socket_.error):
            if self._ssl:
                libssl.SSL_free(self._ssl)
                self._ssl = None
                self._rbio = None
                self._wbio = None
            # The BIOs are freed by SSL_free(), so we only need to free
            # them if for some reason SSL_free() was not called
            else:
                if self._rbio:
                    libssl.BIO_free(self._rbio)
                    self._rbio = None
                if self._wbio:
                    libssl.BIO_free(self._wbio)
                    self._wbio = None
            self.close()

            raise