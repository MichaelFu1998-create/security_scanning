def register_app(self, name, redirect_uri, callback):
        '''
        register_app takes an application name and redirect_uri
        It generates client_id (client_key) and client_secret,
        then stores all of the above in the data_store,
        and returns a dictionary containing the client_id and client_secret.
        '''
        client_id = self._generate_token()
        client_secret = self._generate_token(64)
        yield Task(self.data_store.store, 'applications', client_id=client_id,
                   client_secret=client_secret, name=name,
                   redirect_uri=redirect_uri)
        callback({'client_id':client_id, 'client_secret':client_secret})