def request_authorization(self, client_id, user_id, response_type,
                              redirect_uri=None, scope=None, state=None,
                              expires=600, callback=None):
        '''
        request_authorization generates a nonce, and stores it in the data_store along with the
        client_id, user_id, and expiration timestamp.
        It then returns a dictionary containing the nonce as "code," and the passed
        state.
        ---
        response_type MUST be "code." this is directly from the OAuth2 spec.
        this probably doesn't need to be checked here, but if it's in the spec I
        guess it should be verified somewhere.
        scope has not been implemented here. it will be stored, but there is no
        scope-checking built in here at this time.
        if a redirect_uri is passed, it must match the registered redirect_uri.
        again, this is per spec.
        '''
        if response_type != 'code':
            raise Proauth2Error('invalid_request',
                                'response_type must be "code"', state=state)
        client = yield Task(self.data_store.fetch, 'applications',
                            client_id=client_id)
        if not client: raise Proauth2Error('access_denied')

        if redirect_uri and client['redirect_uri'] != redirect_uri:
            raise Proauth2Error('invalid_request', "redirect_uris don't match")

        nonce_code = self._generate_token()
        expires = time() + expires
        try:
            yield Task(self.data_store.store, 'nonce_codes', code=nonce_code,
                       client_id=client_id, expires=expires, user_id=user_id,
                       scope=scope)
        except Proauth2Error as e:
            e.state = state
            raise e

        callback({'code':nonce_code, 'state':state})