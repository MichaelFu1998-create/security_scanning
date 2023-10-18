def from_json(cls, json_data):
        """Instantiate a Credentials object from a JSON description of it.

        The JSON should have been produced by calling .to_json() on the object.

        Args:
            json_data: string or bytes, JSON to deserialize.

        Returns:
            An instance of a Credentials subclass.
        """
        data = json.loads(_helpers._from_bytes(json_data))
        if (data.get('token_expiry') and
                not isinstance(data['token_expiry'], datetime.datetime)):
            try:
                data['token_expiry'] = datetime.datetime.strptime(
                    data['token_expiry'], EXPIRY_FORMAT)
            except ValueError:
                data['token_expiry'] = None
        retval = cls(
            data['access_token'],
            data['client_id'],
            data['client_secret'],
            data['refresh_token'],
            data['token_expiry'],
            data['token_uri'],
            data['user_agent'],
            revoke_uri=data.get('revoke_uri', None),
            id_token=data.get('id_token', None),
            id_token_jwt=data.get('id_token_jwt', None),
            token_response=data.get('token_response', None),
            scopes=data.get('scopes', None),
            token_info_uri=data.get('token_info_uri', None))
        retval.invalid = data['invalid']
        return retval