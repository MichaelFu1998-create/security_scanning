def sign_message(message, wif, hashfn=hashlib.sha256):
    """ Sign a digest with a wif key

        :param str wif: Private key in
    """

    if not isinstance(message, bytes):
        message = bytes(message, "utf-8")

    digest = hashfn(message).digest()
    priv_key = PrivateKey(wif)
    p = bytes(priv_key)

    if SECP256K1_MODULE == "secp256k1":
        ndata = secp256k1.ffi.new("const int *ndata")
        ndata[0] = 0
        while True:
            ndata[0] += 1
            privkey = secp256k1.PrivateKey(p, raw=True)
            sig = secp256k1.ffi.new("secp256k1_ecdsa_recoverable_signature *")
            signed = secp256k1.lib.secp256k1_ecdsa_sign_recoverable(
                privkey.ctx, sig, digest, privkey.private_key, secp256k1.ffi.NULL, ndata
            )
            if not signed == 1:  # pragma: no cover
                raise AssertionError()
            signature, i = privkey.ecdsa_recoverable_serialize(sig)
            if _is_canonical(signature):
                i += 4  # compressed
                i += 27  # compact
                break
    elif SECP256K1_MODULE == "cryptography":
        cnt = 0
        private_key = ec.derive_private_key(
            int(repr(priv_key), 16), ec.SECP256K1(), default_backend()
        )
        public_key = private_key.public_key()
        while True:
            cnt += 1
            if not cnt % 20:  # pragma: no cover
                log.info(
                    "Still searching for a canonical signature. Tried %d times already!"
                    % cnt
                )
            order = ecdsa.SECP256k1.order
            # signer = private_key.signer(ec.ECDSA(hashes.SHA256()))
            # signer.update(message)
            # sigder = signer.finalize()
            sigder = private_key.sign(message, ec.ECDSA(hashes.SHA256()))
            r, s = decode_dss_signature(sigder)
            signature = ecdsa.util.sigencode_string(r, s, order)
            # Make sure signature is canonical!
            #
            sigder = bytearray(sigder)
            lenR = sigder[3]
            lenS = sigder[5 + lenR]
            if lenR is 32 and lenS is 32:
                # Derive the recovery parameter
                #
                i = recoverPubkeyParameter(message, digest, signature, public_key)
                i += 4  # compressed
                i += 27  # compact
                break
    else:  # pragma: no branch # pragma: no cover
        cnt = 0
        sk = ecdsa.SigningKey.from_string(p, curve=ecdsa.SECP256k1)
        while 1:
            cnt += 1
            if not cnt % 20:  # pragma: no branch
                log.info(
                    "Still searching for a canonical signature. Tried %d times already!"
                    % cnt
                )

            # Deterministic k
            #
            k = ecdsa.rfc6979.generate_k(
                sk.curve.generator.order(),
                sk.privkey.secret_multiplier,
                hashlib.sha256,
                hashlib.sha256(
                    digest
                    + struct.pack(
                        "d", time.time()
                    )  # use the local time to randomize the signature
                ).digest(),
            )

            # Sign message
            #
            sigder = sk.sign_digest(digest, sigencode=ecdsa.util.sigencode_der, k=k)

            # Reformating of signature
            #
            r, s = ecdsa.util.sigdecode_der(sigder, sk.curve.generator.order())
            signature = ecdsa.util.sigencode_string(r, s, sk.curve.generator.order())

            # Make sure signature is canonical!
            #
            sigder = bytearray(sigder)
            lenR = sigder[3]
            lenS = sigder[5 + lenR]
            if lenR is 32 and lenS is 32:
                # Derive the recovery parameter
                #
                i = recoverPubkeyParameter(
                    message, digest, signature, sk.get_verifying_key()
                )
                i += 4  # compressed
                i += 27  # compact
                break

    # pack signature
    #
    sigstr = struct.pack("<B", i)
    sigstr += signature

    return sigstr