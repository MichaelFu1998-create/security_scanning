def encryptPassword(self, login, passwd):
        """Encrypt credentials using the google publickey, with the
        RSA algorithm"""

        # structure of the binary key:
        #
        # *-------------------------------------------------------*
        # | modulus_length | modulus | exponent_length | exponent |
        # *-------------------------------------------------------*
        #
        # modulus_length and exponent_length are uint32
        binaryKey = b64decode(config.GOOGLE_PUBKEY)
        # modulus
        i = utils.readInt(binaryKey, 0)
        modulus = utils.toBigInt(binaryKey[4:][0:i])
        # exponent
        j = utils.readInt(binaryKey, i + 4)
        exponent = utils.toBigInt(binaryKey[i + 8:][0:j])

        # calculate SHA1 of the pub key
        digest = hashes.Hash(hashes.SHA1(), backend=default_backend())
        digest.update(binaryKey)
        h = b'\x00' + digest.finalize()[0:4]

        # generate a public key
        der_data = encode_dss_signature(modulus, exponent)
        publicKey = load_der_public_key(der_data, backend=default_backend())

        # encrypt email and password using pubkey
        to_be_encrypted = login.encode() + b'\x00' + passwd.encode()
        ciphertext = publicKey.encrypt(
            to_be_encrypted,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA1()),
                algorithm=hashes.SHA1(),
                label=None
            )
        )

        return urlsafe_b64encode(h + ciphertext)