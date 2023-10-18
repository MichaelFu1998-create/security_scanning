def request_access_token(self, client_id, key, code, grant_type,
                             redirect_uri=None, method='direct_auth',
                             callback=None):
        '''
        request_access_token validates the client_id and client_secret, using the
        provided method, then generates an access_token, stores it with the user_id
        from the nonce, and returns a dictionary containing an access_token and
        bearer token.
        ---
        from the spec, it looks like there are different types of
        tokens, but i don't understand the disctintions, so someone else can fix
        this if need be.
        regarding the method: it appears that it is intended for there to be
        multiple ways to verify the client_id. my assumption is that you use the
        secret as the salt and pass the hashed of the client_id or something, and
        then compare hashes on the server end. currently the only implemented method
        is direct comparison of the client_ids and client_secrets.
        additional methods can be added to proauth2.auth_methods
        '''
        if grant_type != 'authorization_code':
            raise Proauth2Error('invalid_request',
                                 'grant_type must be "authorization_code"')

        yield Task(self._auth, client_id, key, method)
        user_id = yield Task(self._validate_request_code, code, client_id)
        access_token = self._generate_token(64)
        yield Task(self.data_store.store, 'tokens', token=access_token,
                   user_id=user_id, client_id=client_id)

        callback({'access_token':access_token, 'token_type':'bearer'})