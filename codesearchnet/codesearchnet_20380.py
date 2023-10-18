def gen_dispatch(self, *args, **kwargs):
        '''Find and evaluate/yield every method this input dispatches to.
        '''
        dispatched = False
        for method_data in self.gen_methods(*args, **kwargs):
            dispatched = True

            result = self.apply_handler(method_data, *args, **kwargs)
            yield result
            # return self.yield_from_handler(result)
        if dispatched:
            return
        msg = 'No method was found for %r on %r.'
        raise self.DispatchError(msg % ((args, kwargs), self.inst))