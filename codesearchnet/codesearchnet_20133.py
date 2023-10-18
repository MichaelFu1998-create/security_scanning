def execute(self, args, kwargs):
        '''
        Dispatch a call. Call the first function whose type signature matches
        the arguemts.
        '''
        return self.lookup_explicit(args, kwargs)(*args, **kwargs)