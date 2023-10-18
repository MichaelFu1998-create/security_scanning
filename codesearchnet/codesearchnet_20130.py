def dispatch(self, func):
        '''
        Adds the decorated function to this dispatch.
        '''
        self.callees.append(self._make_dispatch(func))
        return self._make_wrapper(func)