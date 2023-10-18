def _obtain_credentials(self):
        """
        Obtains a credentials handle from secur32.dll for use with SChannel
        """

        protocol_values = {
            'SSLv3': Secur32Const.SP_PROT_SSL3_CLIENT,
            'TLSv1': Secur32Const.SP_PROT_TLS1_CLIENT,
            'TLSv1.1': Secur32Const.SP_PROT_TLS1_1_CLIENT,
            'TLSv1.2': Secur32Const.SP_PROT_TLS1_2_CLIENT,
        }
        protocol_bit_mask = 0
        for key, value in protocol_values.items():
            if key in self._protocols:
                protocol_bit_mask |= value

        algs = [
            Secur32Const.CALG_AES_128,
            Secur32Const.CALG_AES_256,
            Secur32Const.CALG_3DES,
            Secur32Const.CALG_SHA1,
            Secur32Const.CALG_ECDHE,
            Secur32Const.CALG_DH_EPHEM,
            Secur32Const.CALG_RSA_KEYX,
            Secur32Const.CALG_RSA_SIGN,
            Secur32Const.CALG_ECDSA,
            Secur32Const.CALG_DSS_SIGN,
        ]
        if 'TLSv1.2' in self._protocols:
            algs.extend([
                Secur32Const.CALG_SHA512,
                Secur32Const.CALG_SHA384,
                Secur32Const.CALG_SHA256,
            ])

        alg_array = new(secur32, 'ALG_ID[%s]' % len(algs))
        for index, alg in enumerate(algs):
            alg_array[index] = alg

        flags = Secur32Const.SCH_USE_STRONG_CRYPTO | Secur32Const.SCH_CRED_NO_DEFAULT_CREDS
        if not self._manual_validation and not self._extra_trust_roots:
            flags |= Secur32Const.SCH_CRED_AUTO_CRED_VALIDATION
        else:
            flags |= Secur32Const.SCH_CRED_MANUAL_CRED_VALIDATION

        schannel_cred_pointer = struct(secur32, 'SCHANNEL_CRED')
        schannel_cred = unwrap(schannel_cred_pointer)

        schannel_cred.dwVersion = Secur32Const.SCHANNEL_CRED_VERSION
        schannel_cred.cCreds = 0
        schannel_cred.paCred = null()
        schannel_cred.hRootStore = null()
        schannel_cred.cMappers = 0
        schannel_cred.aphMappers = null()
        schannel_cred.cSupportedAlgs = len(alg_array)
        schannel_cred.palgSupportedAlgs = alg_array
        schannel_cred.grbitEnabledProtocols = protocol_bit_mask
        schannel_cred.dwMinimumCipherStrength = 0
        schannel_cred.dwMaximumCipherStrength = 0
        # Default session lifetime is 10 hours
        schannel_cred.dwSessionLifespan = 0
        schannel_cred.dwFlags = flags
        schannel_cred.dwCredFormat = 0

        cred_handle_pointer = new(secur32, 'CredHandle *')

        result = secur32.AcquireCredentialsHandleW(
            null(),
            Secur32Const.UNISP_NAME,
            Secur32Const.SECPKG_CRED_OUTBOUND,
            null(),
            schannel_cred_pointer,
            null(),
            null(),
            cred_handle_pointer,
            null()
        )
        handle_error(result)

        self._credentials_handle = cred_handle_pointer