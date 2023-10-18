def _handshake(self):
        """
        Perform an initial TLS handshake
        """

        session_context = None
        ssl_policy_ref = None
        crl_search_ref = None
        crl_policy_ref = None
        ocsp_search_ref = None
        ocsp_policy_ref = None
        policy_array_ref = None

        try:
            if osx_version_info < (10, 8):
                session_context_pointer = new(Security, 'SSLContextRef *')
                result = Security.SSLNewContext(False, session_context_pointer)
                handle_sec_error(result)
                session_context = unwrap(session_context_pointer)

            else:
                session_context = Security.SSLCreateContext(
                    null(),
                    SecurityConst.kSSLClientSide,
                    SecurityConst.kSSLStreamType
                )

            result = Security.SSLSetIOFuncs(
                session_context,
                _read_callback_pointer,
                _write_callback_pointer
            )
            handle_sec_error(result)

            self._connection_id = id(self) % 2147483647
            _connection_refs[self._connection_id] = self
            _socket_refs[self._connection_id] = self._socket
            result = Security.SSLSetConnection(session_context, self._connection_id)
            handle_sec_error(result)

            utf8_domain = self._hostname.encode('utf-8')
            result = Security.SSLSetPeerDomainName(
                session_context,
                utf8_domain,
                len(utf8_domain)
            )
            handle_sec_error(result)

            if osx_version_info >= (10, 10):
                disable_auto_validation = self._session._manual_validation or self._session._extra_trust_roots
                explicit_validation = (not self._session._manual_validation) and self._session._extra_trust_roots
            else:
                disable_auto_validation = True
                explicit_validation = not self._session._manual_validation

            # Ensure requested protocol support is set for the session
            if osx_version_info < (10, 8):
                for protocol in ['SSLv2', 'SSLv3', 'TLSv1']:
                    protocol_const = _PROTOCOL_STRING_CONST_MAP[protocol]
                    enabled = protocol in self._session._protocols
                    result = Security.SSLSetProtocolVersionEnabled(
                        session_context,
                        protocol_const,
                        enabled
                    )
                    handle_sec_error(result)

                if disable_auto_validation:
                    result = Security.SSLSetEnableCertVerify(session_context, False)
                    handle_sec_error(result)

            else:
                protocol_consts = [_PROTOCOL_STRING_CONST_MAP[protocol] for protocol in self._session._protocols]
                min_protocol = min(protocol_consts)
                max_protocol = max(protocol_consts)
                result = Security.SSLSetProtocolVersionMin(
                    session_context,
                    min_protocol
                )
                handle_sec_error(result)
                result = Security.SSLSetProtocolVersionMax(
                    session_context,
                    max_protocol
                )
                handle_sec_error(result)

                if disable_auto_validation:
                    result = Security.SSLSetSessionOption(
                        session_context,
                        SecurityConst.kSSLSessionOptionBreakOnServerAuth,
                        True
                    )
                    handle_sec_error(result)

            # Disable all sorts of bad cipher suites
            supported_ciphers_pointer = new(Security, 'size_t *')
            result = Security.SSLGetNumberSupportedCiphers(session_context, supported_ciphers_pointer)
            handle_sec_error(result)

            supported_ciphers = deref(supported_ciphers_pointer)

            cipher_buffer = buffer_from_bytes(supported_ciphers * 4)
            supported_cipher_suites_pointer = cast(Security, 'uint32_t *', cipher_buffer)
            result = Security.SSLGetSupportedCiphers(
                session_context,
                supported_cipher_suites_pointer,
                supported_ciphers_pointer
            )
            handle_sec_error(result)

            supported_ciphers = deref(supported_ciphers_pointer)
            supported_cipher_suites = array_from_pointer(
                Security,
                'uint32_t',
                supported_cipher_suites_pointer,
                supported_ciphers
            )
            good_ciphers = []
            for supported_cipher_suite in supported_cipher_suites:
                cipher_suite = int_to_bytes(supported_cipher_suite, width=2)
                cipher_suite_name = CIPHER_SUITE_MAP.get(cipher_suite, cipher_suite)
                good_cipher = _cipher_blacklist_regex.search(cipher_suite_name) is None
                if good_cipher:
                    good_ciphers.append(supported_cipher_suite)

            num_good_ciphers = len(good_ciphers)
            good_ciphers_array = new(Security, 'uint32_t[]', num_good_ciphers)
            array_set(good_ciphers_array, good_ciphers)
            good_ciphers_pointer = cast(Security, 'uint32_t *', good_ciphers_array)
            result = Security.SSLSetEnabledCiphers(
                session_context,
                good_ciphers_pointer,
                num_good_ciphers
            )
            handle_sec_error(result)

            # Set a peer id from the session to allow for session reuse, the hostname
            # is appended to prevent a bug on OS X 10.7 where it tries to reuse a
            # connection even if the hostnames are different.
            peer_id = self._session._peer_id + self._hostname.encode('utf-8')
            result = Security.SSLSetPeerID(session_context, peer_id, len(peer_id))
            handle_sec_error(result)

            handshake_result = Security.SSLHandshake(session_context)
            if self._exception is not None:
                exception = self._exception
                self._exception = None
                raise exception
            while handshake_result == SecurityConst.errSSLWouldBlock:
                handshake_result = Security.SSLHandshake(session_context)
                if self._exception is not None:
                    exception = self._exception
                    self._exception = None
                    raise exception

            if osx_version_info < (10, 8) and osx_version_info >= (10, 7):
                do_validation = explicit_validation and handshake_result == 0
            else:
                do_validation = explicit_validation and handshake_result == SecurityConst.errSSLServerAuthCompleted

            if do_validation:
                trust_ref_pointer = new(Security, 'SecTrustRef *')
                result = Security.SSLCopyPeerTrust(
                    session_context,
                    trust_ref_pointer
                )
                handle_sec_error(result)
                trust_ref = unwrap(trust_ref_pointer)

                cf_string_hostname = CFHelpers.cf_string_from_unicode(self._hostname)
                ssl_policy_ref = Security.SecPolicyCreateSSL(True, cf_string_hostname)
                result = CoreFoundation.CFRelease(cf_string_hostname)
                handle_cf_error(result)

                # Create a new policy for OCSP checking to disable it
                ocsp_oid_pointer = struct(Security, 'CSSM_OID')
                ocsp_oid = unwrap(ocsp_oid_pointer)
                ocsp_oid.Length = len(SecurityConst.APPLE_TP_REVOCATION_OCSP)
                ocsp_oid_buffer = buffer_from_bytes(SecurityConst.APPLE_TP_REVOCATION_OCSP)
                ocsp_oid.Data = cast(Security, 'char *', ocsp_oid_buffer)

                ocsp_search_ref_pointer = new(Security, 'SecPolicySearchRef *')
                result = Security.SecPolicySearchCreate(
                    SecurityConst.CSSM_CERT_X_509v3,
                    ocsp_oid_pointer,
                    null(),
                    ocsp_search_ref_pointer
                )
                handle_sec_error(result)
                ocsp_search_ref = unwrap(ocsp_search_ref_pointer)

                ocsp_policy_ref_pointer = new(Security, 'SecPolicyRef *')
                result = Security.SecPolicySearchCopyNext(ocsp_search_ref, ocsp_policy_ref_pointer)
                handle_sec_error(result)
                ocsp_policy_ref = unwrap(ocsp_policy_ref_pointer)

                ocsp_struct_pointer = struct(Security, 'CSSM_APPLE_TP_OCSP_OPTIONS')
                ocsp_struct = unwrap(ocsp_struct_pointer)
                ocsp_struct.Version = SecurityConst.CSSM_APPLE_TP_OCSP_OPTS_VERSION
                ocsp_struct.Flags = (
                    SecurityConst.CSSM_TP_ACTION_OCSP_DISABLE_NET |
                    SecurityConst.CSSM_TP_ACTION_OCSP_CACHE_READ_DISABLE
                )
                ocsp_struct_bytes = struct_bytes(ocsp_struct_pointer)

                cssm_data_pointer = struct(Security, 'CSSM_DATA')
                cssm_data = unwrap(cssm_data_pointer)
                cssm_data.Length = len(ocsp_struct_bytes)
                ocsp_struct_buffer = buffer_from_bytes(ocsp_struct_bytes)
                cssm_data.Data = cast(Security, 'char *', ocsp_struct_buffer)

                result = Security.SecPolicySetValue(ocsp_policy_ref, cssm_data_pointer)
                handle_sec_error(result)

                # Create a new policy for CRL checking to disable it
                crl_oid_pointer = struct(Security, 'CSSM_OID')
                crl_oid = unwrap(crl_oid_pointer)
                crl_oid.Length = len(SecurityConst.APPLE_TP_REVOCATION_CRL)
                crl_oid_buffer = buffer_from_bytes(SecurityConst.APPLE_TP_REVOCATION_CRL)
                crl_oid.Data = cast(Security, 'char *', crl_oid_buffer)

                crl_search_ref_pointer = new(Security, 'SecPolicySearchRef *')
                result = Security.SecPolicySearchCreate(
                    SecurityConst.CSSM_CERT_X_509v3,
                    crl_oid_pointer,
                    null(),
                    crl_search_ref_pointer
                )
                handle_sec_error(result)
                crl_search_ref = unwrap(crl_search_ref_pointer)

                crl_policy_ref_pointer = new(Security, 'SecPolicyRef *')
                result = Security.SecPolicySearchCopyNext(crl_search_ref, crl_policy_ref_pointer)
                handle_sec_error(result)
                crl_policy_ref = unwrap(crl_policy_ref_pointer)

                crl_struct_pointer = struct(Security, 'CSSM_APPLE_TP_CRL_OPTIONS')
                crl_struct = unwrap(crl_struct_pointer)
                crl_struct.Version = SecurityConst.CSSM_APPLE_TP_CRL_OPTS_VERSION
                crl_struct.CrlFlags = 0
                crl_struct_bytes = struct_bytes(crl_struct_pointer)

                cssm_data_pointer = struct(Security, 'CSSM_DATA')
                cssm_data = unwrap(cssm_data_pointer)
                cssm_data.Length = len(crl_struct_bytes)
                crl_struct_buffer = buffer_from_bytes(crl_struct_bytes)
                cssm_data.Data = cast(Security, 'char *', crl_struct_buffer)

                result = Security.SecPolicySetValue(crl_policy_ref, cssm_data_pointer)
                handle_sec_error(result)

                policy_array_ref = CFHelpers.cf_array_from_list([
                    ssl_policy_ref,
                    crl_policy_ref,
                    ocsp_policy_ref
                ])

                result = Security.SecTrustSetPolicies(trust_ref, policy_array_ref)
                handle_sec_error(result)

                if self._session._extra_trust_roots:
                    ca_cert_refs = []
                    ca_certs = []
                    for cert in self._session._extra_trust_roots:
                        ca_cert = load_certificate(cert)
                        ca_certs.append(ca_cert)
                        ca_cert_refs.append(ca_cert.sec_certificate_ref)

                    result = Security.SecTrustSetAnchorCertificatesOnly(trust_ref, False)
                    handle_sec_error(result)

                    array_ref = CFHelpers.cf_array_from_list(ca_cert_refs)
                    result = Security.SecTrustSetAnchorCertificates(trust_ref, array_ref)
                    handle_sec_error(result)

                result_pointer = new(Security, 'SecTrustResultType *')
                result = Security.SecTrustEvaluate(trust_ref, result_pointer)
                handle_sec_error(result)

                trust_result_code = deref(result_pointer)
                invalid_chain_error_codes = set([
                    SecurityConst.kSecTrustResultProceed,
                    SecurityConst.kSecTrustResultUnspecified
                ])
                if trust_result_code not in invalid_chain_error_codes:
                    handshake_result = SecurityConst.errSSLXCertChainInvalid
                else:
                    handshake_result = Security.SSLHandshake(session_context)
                    while handshake_result == SecurityConst.errSSLWouldBlock:
                        handshake_result = Security.SSLHandshake(session_context)

            self._done_handshake = True

            handshake_error_codes = set([
                SecurityConst.errSSLXCertChainInvalid,
                SecurityConst.errSSLCertExpired,
                SecurityConst.errSSLCertNotYetValid,
                SecurityConst.errSSLUnknownRootCert,
                SecurityConst.errSSLNoRootCert,
                SecurityConst.errSSLHostNameMismatch,
                SecurityConst.errSSLInternal,
            ])

            # In testing, only errSSLXCertChainInvalid was ever returned for
            # all of these different situations, however we include the others
            # for completeness. To get the real reason we have to use the
            # certificate from the handshake and use the deprecated function
            # SecTrustGetCssmResultCode().
            if handshake_result in handshake_error_codes:
                trust_ref_pointer = new(Security, 'SecTrustRef *')
                result = Security.SSLCopyPeerTrust(
                    session_context,
                    trust_ref_pointer
                )
                handle_sec_error(result)
                trust_ref = unwrap(trust_ref_pointer)

                result_code_pointer = new(Security, 'OSStatus *')
                result = Security.SecTrustGetCssmResultCode(trust_ref, result_code_pointer)
                result_code = deref(result_code_pointer)

                chain = extract_chain(self._server_hello)

                self_signed = False
                revoked = False
                expired = False
                not_yet_valid = False
                no_issuer = False
                cert = None
                bad_hostname = False

                if chain:
                    cert = chain[0]
                    oscrypto_cert = load_certificate(cert)
                    self_signed = oscrypto_cert.self_signed
                    revoked = result_code == SecurityConst.CSSMERR_TP_CERT_REVOKED
                    no_issuer = not self_signed and result_code == SecurityConst.CSSMERR_TP_NOT_TRUSTED
                    expired = result_code == SecurityConst.CSSMERR_TP_CERT_EXPIRED
                    not_yet_valid = result_code == SecurityConst.CSSMERR_TP_CERT_NOT_VALID_YET
                    bad_hostname = result_code == SecurityConst.CSSMERR_APPLETP_HOSTNAME_MISMATCH

                    # On macOS 10.12, some expired certificates return errSSLInternal
                    if osx_version_info >= (10, 12):
                        validity = cert['tbs_certificate']['validity']
                        not_before = validity['not_before'].chosen.native
                        not_after = validity['not_after'].chosen.native
                        utcnow = datetime.datetime.now(timezone.utc)
                        expired = not_after < utcnow
                        not_yet_valid = not_before > utcnow

                if chain and chain[0].hash_algo in set(['md5', 'md2']):
                    raise_weak_signature(chain[0])

                if revoked:
                    raise_revoked(cert)

                if bad_hostname:
                    raise_hostname(cert, self._hostname)

                elif expired or not_yet_valid:
                    raise_expired_not_yet_valid(cert)

                elif no_issuer:
                    raise_no_issuer(cert)

                elif self_signed:
                    raise_self_signed(cert)

                if detect_client_auth_request(self._server_hello):
                    raise_client_auth()

                raise_verification(cert)

            if handshake_result == SecurityConst.errSSLPeerHandshakeFail:
                if detect_client_auth_request(self._server_hello):
                    raise_client_auth()
                raise_handshake()

            if handshake_result == SecurityConst.errSSLWeakPeerEphemeralDHKey:
                raise_dh_params()

            if handshake_result == SecurityConst.errSSLPeerProtocolVersion:
                raise_protocol_version()

            if handshake_result in set([SecurityConst.errSSLRecordOverflow, SecurityConst.errSSLProtocol]):
                self._server_hello += _read_remaining(self._socket)
                raise_protocol_error(self._server_hello)

            if handshake_result in set([SecurityConst.errSSLClosedNoNotify, SecurityConst.errSSLClosedAbort]):
                if not self._done_handshake:
                    self._server_hello += _read_remaining(self._socket)
                if detect_other_protocol(self._server_hello):
                    raise_protocol_error(self._server_hello)
                raise_disconnection()

            if osx_version_info < (10, 10):
                dh_params_length = get_dh_params_length(self._server_hello)
                if dh_params_length is not None and dh_params_length < 1024:
                    raise_dh_params()

            would_block = handshake_result == SecurityConst.errSSLWouldBlock
            server_auth_complete = handshake_result == SecurityConst.errSSLServerAuthCompleted
            manual_validation = self._session._manual_validation and server_auth_complete
            if not would_block and not manual_validation:
                handle_sec_error(handshake_result, TLSError)

            self._session_context = session_context

            protocol_const_pointer = new(Security, 'SSLProtocol *')
            result = Security.SSLGetNegotiatedProtocolVersion(
                session_context,
                protocol_const_pointer
            )
            handle_sec_error(result)
            protocol_const = deref(protocol_const_pointer)

            self._protocol = _PROTOCOL_CONST_STRING_MAP[protocol_const]

            cipher_int_pointer = new(Security, 'SSLCipherSuite *')
            result = Security.SSLGetNegotiatedCipher(
                session_context,
                cipher_int_pointer
            )
            handle_sec_error(result)
            cipher_int = deref(cipher_int_pointer)

            cipher_bytes = int_to_bytes(cipher_int, width=2)
            self._cipher_suite = CIPHER_SUITE_MAP.get(cipher_bytes, cipher_bytes)

            session_info = parse_session_info(
                self._server_hello,
                self._client_hello
            )
            self._compression = session_info['compression']
            self._session_id = session_info['session_id']
            self._session_ticket = session_info['session_ticket']

        except (OSError, socket_.error):
            if session_context:
                if osx_version_info < (10, 8):
                    result = Security.SSLDisposeContext(session_context)
                    handle_sec_error(result)
                else:
                    result = CoreFoundation.CFRelease(session_context)
                    handle_cf_error(result)

            self._session_context = None
            self.close()

            raise

        finally:
            # Trying to release crl_search_ref or ocsp_search_ref results in
            # a segmentation fault, so we do not do that

            if ssl_policy_ref:
                result = CoreFoundation.CFRelease(ssl_policy_ref)
                handle_cf_error(result)
                ssl_policy_ref = None

            if crl_policy_ref:
                result = CoreFoundation.CFRelease(crl_policy_ref)
                handle_cf_error(result)
                crl_policy_ref = None

            if ocsp_policy_ref:
                result = CoreFoundation.CFRelease(ocsp_policy_ref)
                handle_cf_error(result)
                ocsp_policy_ref = None

            if policy_array_ref:
                result = CoreFoundation.CFRelease(policy_array_ref)
                handle_cf_error(result)
                policy_array_ref = None