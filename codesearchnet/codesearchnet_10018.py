def _handshake(self, renegotiate=False):
        """
        Perform an initial TLS handshake, or a renegotiation

        :param renegotiate:
            If the handshake is for a renegotiation
        """

        in_buffers = None
        out_buffers = None
        new_context_handle_pointer = None

        try:
            if renegotiate:
                temp_context_handle_pointer = self._context_handle_pointer
            else:
                new_context_handle_pointer = new(secur32, 'CtxtHandle *')
                temp_context_handle_pointer = new_context_handle_pointer

            requested_flags = {
                Secur32Const.ISC_REQ_REPLAY_DETECT: 'replay detection',
                Secur32Const.ISC_REQ_SEQUENCE_DETECT: 'sequence detection',
                Secur32Const.ISC_REQ_CONFIDENTIALITY: 'confidentiality',
                Secur32Const.ISC_REQ_ALLOCATE_MEMORY: 'memory allocation',
                Secur32Const.ISC_REQ_INTEGRITY: 'integrity',
                Secur32Const.ISC_REQ_STREAM: 'stream orientation',
                Secur32Const.ISC_REQ_USE_SUPPLIED_CREDS: 'disable automatic client auth',
            }

            self._context_flags = 0
            for flag in requested_flags:
                self._context_flags |= flag

            in_sec_buffer_desc_pointer, in_buffers = self._create_buffers(2)
            in_buffers[0].BufferType = Secur32Const.SECBUFFER_TOKEN

            out_sec_buffer_desc_pointer, out_buffers = self._create_buffers(2)
            out_buffers[0].BufferType = Secur32Const.SECBUFFER_TOKEN
            out_buffers[1].BufferType = Secur32Const.SECBUFFER_ALERT

            output_context_flags_pointer = new(secur32, 'ULONG *')

            if renegotiate:
                first_handle = temp_context_handle_pointer
                second_handle = null()
            else:
                first_handle = null()
                second_handle = temp_context_handle_pointer

            result = secur32.InitializeSecurityContextW(
                self._session._credentials_handle,
                first_handle,
                self._hostname,
                self._context_flags,
                0,
                0,
                null(),
                0,
                second_handle,
                out_sec_buffer_desc_pointer,
                output_context_flags_pointer,
                null()
            )
            if result not in set([Secur32Const.SEC_E_OK, Secur32Const.SEC_I_CONTINUE_NEEDED]):
                handle_error(result, TLSError)

            if not renegotiate:
                temp_context_handle_pointer = second_handle
            else:
                temp_context_handle_pointer = first_handle

            handshake_server_bytes = b''
            handshake_client_bytes = b''

            if out_buffers[0].cbBuffer > 0:
                token = bytes_from_buffer(out_buffers[0].pvBuffer, out_buffers[0].cbBuffer)
                handshake_client_bytes += token
                self._socket.send(token)
                out_buffers[0].cbBuffer = 0
                secur32.FreeContextBuffer(out_buffers[0].pvBuffer)
                out_buffers[0].pvBuffer = null()

            in_data_buffer = buffer_from_bytes(32768)
            in_buffers[0].pvBuffer = cast(secur32, 'BYTE *', in_data_buffer)

            bytes_read = b''
            while result != Secur32Const.SEC_E_OK:
                try:
                    fail_late = False
                    bytes_read = self._socket.recv(8192)
                    if bytes_read == b'':
                        raise_disconnection()
                except (socket_error_cls):
                    fail_late = True
                handshake_server_bytes += bytes_read
                self._received_bytes += bytes_read

                in_buffers[0].cbBuffer = len(self._received_bytes)
                write_to_buffer(in_data_buffer, self._received_bytes)

                result = secur32.InitializeSecurityContextW(
                    self._session._credentials_handle,
                    temp_context_handle_pointer,
                    self._hostname,
                    self._context_flags,
                    0,
                    0,
                    in_sec_buffer_desc_pointer,
                    0,
                    null(),
                    out_sec_buffer_desc_pointer,
                    output_context_flags_pointer,
                    null()
                )

                if result == Secur32Const.SEC_E_INCOMPLETE_MESSAGE:
                    in_buffers[0].BufferType = Secur32Const.SECBUFFER_TOKEN
                    # Windows 10 seems to fill the second input buffer with
                    # a BufferType of SECBUFFER_MISSING (4), which if not
                    # cleared causes the handshake to fail.
                    if in_buffers[1].BufferType != Secur32Const.SECBUFFER_EMPTY:
                        in_buffers[1].BufferType = Secur32Const.SECBUFFER_EMPTY
                        in_buffers[1].cbBuffer = 0
                        if not is_null(in_buffers[1].pvBuffer):
                            secur32.FreeContextBuffer(in_buffers[1].pvBuffer)
                            in_buffers[1].pvBuffer = null()

                    if fail_late:
                        raise_disconnection()

                    continue

                if result == Secur32Const.SEC_E_ILLEGAL_MESSAGE:
                    if detect_client_auth_request(handshake_server_bytes):
                        raise_client_auth()
                    alert_info = parse_alert(handshake_server_bytes)
                    if alert_info and alert_info == (2, 70):
                        raise_protocol_version()
                    raise_handshake()

                if result == Secur32Const.SEC_E_WRONG_PRINCIPAL:
                    chain = extract_chain(handshake_server_bytes)
                    raise_hostname(chain[0], self._hostname)

                if result == Secur32Const.SEC_E_CERT_EXPIRED:
                    chain = extract_chain(handshake_server_bytes)
                    raise_expired_not_yet_valid(chain[0])

                if result == Secur32Const.SEC_E_UNTRUSTED_ROOT:
                    chain = extract_chain(handshake_server_bytes)
                    cert = chain[0]
                    oscrypto_cert = load_certificate(cert)
                    if not oscrypto_cert.self_signed:
                        raise_no_issuer(cert)
                    raise_self_signed(cert)

                if result == Secur32Const.SEC_E_INTERNAL_ERROR:
                    if get_dh_params_length(handshake_server_bytes) < 1024:
                        raise_dh_params()

                if result == Secur32Const.SEC_I_INCOMPLETE_CREDENTIALS:
                    raise_client_auth()

                if result == Crypt32Const.TRUST_E_CERT_SIGNATURE:
                    raise_weak_signature(cert)

                if result == Secur32Const.SEC_E_INVALID_TOKEN:
                    # If an alert it present, there may have been a handshake
                    # error due to the server using a certificate path with a
                    # trust root using MD2 or MD5 combined with TLS 1.2. To
                    # work around this, if the user allows anything other than
                    # TLS 1.2, we just remove it from the acceptable protocols
                    # and try again.
                    if out_buffers[1].cbBuffer > 0:
                        alert_bytes = bytes_from_buffer(out_buffers[1].pvBuffer, out_buffers[1].cbBuffer)
                        handshake_client_bytes += alert_bytes
                        alert_number = alert_bytes[6:7]
                        if alert_number == b'\x28' or alert_number == b'\x2b':
                            if 'TLSv1.2' in self._session._protocols and len(self._session._protocols) > 1:
                                chain = extract_chain(handshake_server_bytes)
                                raise _TLSDowngradeError(
                                    'Server certificate verification failed - weak certificate signature algorithm',
                                    chain[0]
                                )
                    if detect_client_auth_request(handshake_server_bytes):
                        raise_client_auth()
                    if detect_other_protocol(handshake_server_bytes):
                        raise_protocol_error(handshake_server_bytes)
                    raise_handshake()

                # These are semi-common errors with TLSv1.2 on Windows 7 an 8
                # that appears to be due to poor handling of the
                # ServerKeyExchange for DHE_RSA cipher suites. The solution
                # is to retry the handshake.
                if result == Secur32Const.SEC_E_BUFFER_TOO_SMALL or result == Secur32Const.SEC_E_MESSAGE_ALTERED:
                    if 'TLSv1.2' in self._session._protocols:
                        raise _TLSRetryError('TLS handshake failed')

                if fail_late:
                    raise_disconnection()

                if result == Secur32Const.SEC_E_INVALID_PARAMETER:
                    if get_dh_params_length(handshake_server_bytes) < 1024:
                        raise_dh_params()

                if result not in set([Secur32Const.SEC_E_OK, Secur32Const.SEC_I_CONTINUE_NEEDED]):
                    handle_error(result, TLSError)

                if out_buffers[0].cbBuffer > 0:
                    token = bytes_from_buffer(out_buffers[0].pvBuffer, out_buffers[0].cbBuffer)
                    handshake_client_bytes += token
                    self._socket.send(token)
                    out_buffers[0].cbBuffer = 0
                    secur32.FreeContextBuffer(out_buffers[0].pvBuffer)
                    out_buffers[0].pvBuffer = null()

                if in_buffers[1].BufferType == Secur32Const.SECBUFFER_EXTRA:
                    extra_amount = in_buffers[1].cbBuffer
                    self._received_bytes = self._received_bytes[-extra_amount:]
                    in_buffers[1].BufferType = Secur32Const.SECBUFFER_EMPTY
                    in_buffers[1].cbBuffer = 0
                    secur32.FreeContextBuffer(in_buffers[1].pvBuffer)
                    in_buffers[1].pvBuffer = null()

                    # The handshake is complete, so discard any extra bytes
                    if result == Secur32Const.SEC_E_OK:
                        handshake_server_bytes = handshake_server_bytes[-extra_amount:]

                else:
                    self._received_bytes = b''

            connection_info_pointer = struct(secur32, 'SecPkgContext_ConnectionInfo')
            result = secur32.QueryContextAttributesW(
                temp_context_handle_pointer,
                Secur32Const.SECPKG_ATTR_CONNECTION_INFO,
                connection_info_pointer
            )
            handle_error(result, TLSError)

            connection_info = unwrap(connection_info_pointer)

            self._protocol = {
                Secur32Const.SP_PROT_SSL2_CLIENT: 'SSLv2',
                Secur32Const.SP_PROT_SSL3_CLIENT: 'SSLv3',
                Secur32Const.SP_PROT_TLS1_CLIENT: 'TLSv1',
                Secur32Const.SP_PROT_TLS1_1_CLIENT: 'TLSv1.1',
                Secur32Const.SP_PROT_TLS1_2_CLIENT: 'TLSv1.2',
            }.get(native(int, connection_info.dwProtocol), str_cls(connection_info.dwProtocol))

            if self._protocol in set(['SSLv3', 'TLSv1', 'TLSv1.1', 'TLSv1.2']):
                session_info = parse_session_info(handshake_server_bytes, handshake_client_bytes)
                self._cipher_suite = session_info['cipher_suite']
                self._compression = session_info['compression']
                self._session_id = session_info['session_id']
                self._session_ticket = session_info['session_ticket']

            output_context_flags = deref(output_context_flags_pointer)

            for flag in requested_flags:
                if (flag | output_context_flags) == 0:
                    raise OSError(pretty_message(
                        '''
                        Unable to obtain a credential context with the property %s
                        ''',
                        requested_flags[flag]
                    ))

            if not renegotiate:
                self._context_handle_pointer = temp_context_handle_pointer
                new_context_handle_pointer = None

                stream_sizes_pointer = struct(secur32, 'SecPkgContext_StreamSizes')
                result = secur32.QueryContextAttributesW(
                    self._context_handle_pointer,
                    Secur32Const.SECPKG_ATTR_STREAM_SIZES,
                    stream_sizes_pointer
                )
                handle_error(result)

                stream_sizes = unwrap(stream_sizes_pointer)
                self._header_size = native(int, stream_sizes.cbHeader)
                self._message_size = native(int, stream_sizes.cbMaximumMessage)
                self._trailer_size = native(int, stream_sizes.cbTrailer)
                self._buffer_size = self._header_size + self._message_size + self._trailer_size

            if self._session._extra_trust_roots:
                self._extra_trust_root_validation()

        except (OSError, socket_.error):
            self.close()

            raise

        finally:
            if out_buffers:
                if not is_null(out_buffers[0].pvBuffer):
                    secur32.FreeContextBuffer(out_buffers[0].pvBuffer)
                if not is_null(out_buffers[1].pvBuffer):
                    secur32.FreeContextBuffer(out_buffers[1].pvBuffer)
            if new_context_handle_pointer:
                secur32.DeleteSecurityContext(new_context_handle_pointer)