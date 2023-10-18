def dispatch(self, *args, **kwargs):
        '''Find and evaluate/return the first method this input dispatches to.
        '''
        for result in self.gen_dispatch(*args, **kwargs):
            return result