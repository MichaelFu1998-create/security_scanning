def dispatch_first(self, func):
        '''
        Adds the decorated function to this dispatch, at the FRONT of the order.
        Useful for allowing third parties to add overloaded functionality
        to be executed before default functionality.
        '''
        self.callees.appendleft(self._make_dispatch(func))
        return self._make_wrapper(func)