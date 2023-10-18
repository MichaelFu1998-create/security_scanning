def _validate_request_code(self, code, client_id, callback):
        '''
        _validate_request_code - internal method for verifying the the given nonce.
        also removes the nonce from the data_store, as they are intended for
        one-time use.
        '''
        nonce = yield Task(self.data_store.fetch, 'nonce_codes', code=code)
        if not nonce:
            raise Proauth2Error('access_denied', 'invalid request code: %s' % code)
        if client_id != nonce['client_id']: 
            raise Proauth2Error('access_denied', 'invalid request code: %s' % code)
        user_id = nonce['user_id']
        expires = nonce['expires']
        yield Task(self.data_store.remove, 'nonce_codes', code=code,
                   client_id=client_id, user_id=user_id)

        if time() > expires:
            raise Proauth2Error('access_denied', 'request code %s expired' % code)

        callback(user_id)