def _make_wrapper(self, func):
        '''
        Makes a wrapper function that executes a dispatch call for func. The
        wrapper has the dispatch and dispatch_first attributes, so that
        additional overloads can be added to the group.
        '''

        #TODO: consider using a class to make attribute forwarding easier.
        #TODO: consider using simply another DispatchGroup, with self.callees
        # assigned by reference to the original callees.
        @wraps(func)
        def executor(*args, **kwargs):
            return self.execute(args, kwargs)
        executor.dispatch = self.dispatch
        executor.dispatch_first = self.dispatch_first
        executor.func = func
        executor.lookup = self.lookup
        return executor