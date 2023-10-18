def from_json(cls, json_data):
        """Deserialize a JSON-serialized instance.

        Inverse to :meth:`to_json`.

        Args:
            json_data: dict or string, Serialized JSON (as a string or an
                       already parsed dictionary) representing a credential.

        Returns:
            ServiceAccountCredentials from the serialized data.
        """
        if not isinstance(json_data, dict):
            json_data = json.loads(_helpers._from_bytes(json_data))

        private_key_pkcs8_pem = None
        pkcs12_val = json_data.get(_PKCS12_KEY)
        password = None
        if pkcs12_val is None:
            private_key_pkcs8_pem = json_data['_private_key_pkcs8_pem']
            signer = crypt.Signer.from_string(private_key_pkcs8_pem)
        else:
            # NOTE: This assumes that private_key_pkcs8_pem is not also
            #       in the serialized data. This would be very incorrect
            #       state.
            pkcs12_val = base64.b64decode(pkcs12_val)
            password = json_data['_private_key_password']
            signer = crypt.Signer.from_string(pkcs12_val, password)

        credentials = cls(
            json_data['_service_account_email'],
            signer,
            scopes=json_data['_scopes'],
            private_key_id=json_data['_private_key_id'],
            client_id=json_data['client_id'],
            user_agent=json_data['_user_agent'],
            **json_data['_kwargs']
        )
        if private_key_pkcs8_pem is not None:
            credentials._private_key_pkcs8_pem = private_key_pkcs8_pem
        if pkcs12_val is not None:
            credentials._private_key_pkcs12 = pkcs12_val
        if password is not None:
            credentials._private_key_password = password
        credentials.invalid = json_data['invalid']
        credentials.access_token = json_data['access_token']
        credentials.token_uri = json_data['token_uri']
        credentials.revoke_uri = json_data['revoke_uri']
        token_expiry = json_data.get('token_expiry', None)
        if token_expiry is not None:
            credentials.token_expiry = datetime.datetime.strptime(
                token_expiry, client.EXPIRY_FORMAT)
        return credentials