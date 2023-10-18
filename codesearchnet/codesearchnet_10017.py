def _extra_trust_root_validation(self):
        """
        Manually invoked windows certificate chain builder and verification
        step when there are extra trust roots to include in the search process
        """

        store = None
        cert_chain_context_pointer = None

        try:
            # We set up an in-memory store to pass as an extra store to grab
            # certificates from when performing the verification
            store = crypt32.CertOpenStore(
                Crypt32Const.CERT_STORE_PROV_MEMORY,
                Crypt32Const.X509_ASN_ENCODING,
                null(),
                0,
                null()
            )
            if is_null(store):
                handle_crypt32_error(0)

            cert_hashes = set()
            for cert in self._session._extra_trust_roots:
                cert_data = cert.dump()
                result = crypt32.CertAddEncodedCertificateToStore(
                    store,
                    Crypt32Const.X509_ASN_ENCODING,
                    cert_data,
                    len(cert_data),
                    Crypt32Const.CERT_STORE_ADD_USE_EXISTING,
                    null()
                )
                if not result:
                    handle_crypt32_error(0)
                cert_hashes.add(cert.sha256)

            cert_context_pointer_pointer = new(crypt32, 'PCERT_CONTEXT *')
            result = secur32.QueryContextAttributesW(
                self._context_handle_pointer,
                Secur32Const.SECPKG_ATTR_REMOTE_CERT_CONTEXT,
                cert_context_pointer_pointer
            )
            handle_error(result)

            cert_context_pointer = unwrap(cert_context_pointer_pointer)
            cert_context_pointer = cast(crypt32, 'PCERT_CONTEXT', cert_context_pointer)

            # We have to do a funky shuffle here because FILETIME from kernel32
            # is different than FILETIME from crypt32 when using cffi. If we
            # overwrite the "now_pointer" variable, cffi releases the backing
            # memory and we end up getting a validation error about certificate
            # expiration time.
            orig_now_pointer = new(kernel32, 'FILETIME *')
            kernel32.GetSystemTimeAsFileTime(orig_now_pointer)
            now_pointer = cast(crypt32, 'FILETIME *', orig_now_pointer)

            usage_identifiers = new(crypt32, 'char *[3]')
            usage_identifiers[0] = cast(crypt32, 'char *', Crypt32Const.PKIX_KP_SERVER_AUTH)
            usage_identifiers[1] = cast(crypt32, 'char *', Crypt32Const.SERVER_GATED_CRYPTO)
            usage_identifiers[2] = cast(crypt32, 'char *', Crypt32Const.SGC_NETSCAPE)

            cert_enhkey_usage_pointer = struct(crypt32, 'CERT_ENHKEY_USAGE')
            cert_enhkey_usage = unwrap(cert_enhkey_usage_pointer)
            cert_enhkey_usage.cUsageIdentifier = 3
            cert_enhkey_usage.rgpszUsageIdentifier = cast(crypt32, 'char **', usage_identifiers)

            cert_usage_match_pointer = struct(crypt32, 'CERT_USAGE_MATCH')
            cert_usage_match = unwrap(cert_usage_match_pointer)
            cert_usage_match.dwType = Crypt32Const.USAGE_MATCH_TYPE_OR
            cert_usage_match.Usage = cert_enhkey_usage

            cert_chain_para_pointer = struct(crypt32, 'CERT_CHAIN_PARA')
            cert_chain_para = unwrap(cert_chain_para_pointer)
            cert_chain_para.RequestedUsage = cert_usage_match
            cert_chain_para_size = sizeof(crypt32, cert_chain_para)
            cert_chain_para.cbSize = cert_chain_para_size

            cert_chain_context_pointer_pointer = new(crypt32, 'PCERT_CHAIN_CONTEXT *')
            result = crypt32.CertGetCertificateChain(
                null(),
                cert_context_pointer,
                now_pointer,
                store,
                cert_chain_para_pointer,
                Crypt32Const.CERT_CHAIN_CACHE_END_CERT | Crypt32Const.CERT_CHAIN_REVOCATION_CHECK_CACHE_ONLY,
                null(),
                cert_chain_context_pointer_pointer
            )
            handle_crypt32_error(result)

            cert_chain_policy_para_flags = Crypt32Const.CERT_CHAIN_POLICY_IGNORE_ALL_REV_UNKNOWN_FLAGS

            cert_chain_context_pointer = unwrap(cert_chain_context_pointer_pointer)

            # Unwrap the chain and if the final element in the chain is one of
            # extra trust roots, set flags so that we trust the certificate even
            # though it is not in the Trusted Roots store
            cert_chain_context = unwrap(cert_chain_context_pointer)
            num_chains = native(int, cert_chain_context.cChain)
            if num_chains == 1:
                first_simple_chain_pointer = unwrap(cert_chain_context.rgpChain)
                first_simple_chain = unwrap(first_simple_chain_pointer)
                num_elements = native(int, first_simple_chain.cElement)
                last_element_pointer = first_simple_chain.rgpElement[num_elements - 1]
                last_element = unwrap(last_element_pointer)
                last_element_cert = unwrap(last_element.pCertContext)
                last_element_cert_data = bytes_from_buffer(
                    last_element_cert.pbCertEncoded,
                    native(int, last_element_cert.cbCertEncoded)
                )
                last_cert = x509.Certificate.load(last_element_cert_data)
                if last_cert.sha256 in cert_hashes:
                    cert_chain_policy_para_flags |= Crypt32Const.CERT_CHAIN_POLICY_ALLOW_UNKNOWN_CA_FLAG

            ssl_extra_cert_chain_policy_para_pointer = struct(crypt32, 'SSL_EXTRA_CERT_CHAIN_POLICY_PARA')
            ssl_extra_cert_chain_policy_para = unwrap(ssl_extra_cert_chain_policy_para_pointer)
            ssl_extra_cert_chain_policy_para.cbSize = sizeof(crypt32, ssl_extra_cert_chain_policy_para)
            ssl_extra_cert_chain_policy_para.dwAuthType = Crypt32Const.AUTHTYPE_SERVER
            ssl_extra_cert_chain_policy_para.fdwChecks = 0
            ssl_extra_cert_chain_policy_para.pwszServerName = cast(
                crypt32,
                'wchar_t *',
                buffer_from_unicode(self._hostname)
            )

            cert_chain_policy_para_pointer = struct(crypt32, 'CERT_CHAIN_POLICY_PARA')
            cert_chain_policy_para = unwrap(cert_chain_policy_para_pointer)
            cert_chain_policy_para.cbSize = sizeof(crypt32, cert_chain_policy_para)
            cert_chain_policy_para.dwFlags = cert_chain_policy_para_flags
            cert_chain_policy_para.pvExtraPolicyPara = cast(crypt32, 'void *', ssl_extra_cert_chain_policy_para_pointer)

            cert_chain_policy_status_pointer = struct(crypt32, 'CERT_CHAIN_POLICY_STATUS')
            cert_chain_policy_status = unwrap(cert_chain_policy_status_pointer)
            cert_chain_policy_status.cbSize = sizeof(crypt32, cert_chain_policy_status)

            result = crypt32.CertVerifyCertificateChainPolicy(
                Crypt32Const.CERT_CHAIN_POLICY_SSL,
                cert_chain_context_pointer,
                cert_chain_policy_para_pointer,
                cert_chain_policy_status_pointer
            )
            handle_crypt32_error(result)

            cert_context = unwrap(cert_context_pointer)
            cert_data = bytes_from_buffer(cert_context.pbCertEncoded, native(int, cert_context.cbCertEncoded))
            cert = x509.Certificate.load(cert_data)

            error = cert_chain_policy_status.dwError
            if error:
                if error == Crypt32Const.CERT_E_EXPIRED:
                    raise_expired_not_yet_valid(cert)
                if error == Crypt32Const.CERT_E_UNTRUSTEDROOT:
                    oscrypto_cert = load_certificate(cert)
                    if oscrypto_cert.self_signed:
                        raise_self_signed(cert)
                    else:
                        raise_no_issuer(cert)
                if error == Crypt32Const.CERT_E_CN_NO_MATCH:
                    raise_hostname(cert, self._hostname)

                if error == Crypt32Const.TRUST_E_CERT_SIGNATURE:
                    raise_weak_signature(cert)

                if error == Crypt32Const.CRYPT_E_REVOKED:
                    raise_revoked(cert)

                raise_verification(cert)

            if cert.hash_algo in set(['md5', 'md2']):
                raise_weak_signature(cert)

        finally:
            if store:
                crypt32.CertCloseStore(store, 0)
            if cert_chain_context_pointer:
                crypt32.CertFreeCertificateChain(cert_chain_context_pointer)