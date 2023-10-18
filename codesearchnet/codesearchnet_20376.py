def register(self, method, args, kwargs):
        '''Given a single decorated handler function,
        prepare, append desired data to self.registry.
        '''
        invoc = self.dump_invoc(*args, **kwargs)
        self.registry.append((invoc, method.__name__))