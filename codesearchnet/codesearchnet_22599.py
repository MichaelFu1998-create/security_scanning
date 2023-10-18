def _auth(self, client_id, key, method, callback):
        '''
        _auth - internal method to ensure the client_id and client_secret passed with
        the nonce match
        '''
        available = auth_methods.keys()
        if method not in available:
            raise Proauth2Error('invalid_request',
                                'unsupported authentication method: %s'
                                'available methods: %s' % \
                                (method, '\n'.join(available)))
        client = yield Task(self.data_store.fetch, 'applications',
                            client_id=client_id)
        if not client: raise Proauth2Error('access_denied')
        if not auth_methods[method](key, client['client_secret']):
            raise Proauth2Error('access_denied')
        callback()