def get_method(self, *args, **kwargs):
        '''Find the first method this input dispatches to.
        '''
        for method in self.gen_methods(*args, **kwargs):
            return method
        msg = 'No method was found for %r on %r.'
        raise self.DispatchError(msg % ((args, kwargs), self.inst))