def _retrieve_certificate(self, access_token, timeout=3):
        """
        Generates a new private key and certificate request, submits the request to be
        signed by the SLCS CA and returns the certificate.
        """
        logger.debug("Retrieve certificate with token.")

        # Generate a new key pair
        key_pair = crypto.PKey()
        key_pair.generate_key(crypto.TYPE_RSA, 2048)
        private_key = crypto.dump_privatekey(crypto.FILETYPE_PEM, key_pair).decode("utf-8")

        # Generate a certificate request using that key-pair
        cert_request = crypto.X509Req()

        # Create public key object
        cert_request.set_pubkey(key_pair)

        # Add the public key to the request
        cert_request.sign(key_pair, 'md5')
        der_cert_req = crypto.dump_certificate_request(crypto.FILETYPE_ASN1, cert_request)

        encoded_cert_req = base64.b64encode(der_cert_req)

        # Build the OAuth session object
        token = {'access_token': access_token, 'token_type': 'Bearer'}
        client = OAuth2Session(token=token)

        response = client.post(
            self.certificate_url,
            data={'certificate_request': encoded_cert_req},
            verify=False,
            timeout=timeout,
        )

        if response.ok:
            content = "{} {}".format(response.text, private_key)
            with open(self.esgf_credentials, 'w') as fh:
                fh.write(content)
            logger.debug('Fetched certificate successfully.')
        else:
            msg = "Could not get certificate: {} {}".format(response.status_code, response.reason)
            raise Exception(msg)
        return True