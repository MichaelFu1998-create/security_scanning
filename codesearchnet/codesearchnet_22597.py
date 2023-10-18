def authenticate_token(self, token, callback):
        '''
        authenticate_token checks the passed token and returns the user_id it is
        associated with. it is assumed that this method won't be directly exposed to
        the oauth client, but some kind of framework or wrapper. this allows the
        framework to have the user_id without doing additional DB calls.
        '''
        token_data = yield Task(self.data_store.fetch, 'tokens', token=token)
        if not token_data:
            raise Proauth2Error('access_denied',
                                'token does not exist or has been revoked')
        callback(token_data['user_id'])