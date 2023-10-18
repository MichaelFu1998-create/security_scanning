def revoke_token(self, token, callback):
        '''
        revoke_token removes the access token from the data_store
        '''
        yield Task(self.data_store.remove, 'tokens', token=token)
        callback()