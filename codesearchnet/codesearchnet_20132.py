def lookup_explicit(self, args, kwargs):
        '''
        Lookup the function that will be called with a given set of arguments,
        or raise DispatchError. Requires explicit tuple/dict grouping of
        arguments (see DispatchGroup.lookup for a function-like interface).
        '''
        for bind_args, callee in self.callees:
            try:
                #bind to the signature and types. Raises TypeError on failure
                bind_args(args, kwargs)
            except TypeError:
                #TypeError: failed to bind arguments. Try the next dispatch
                continue

            #All the parameters matched. Return the function and args
            return callee

        else:
            #Nothing was able to bind. Error.
            raise DispatchError(args, kwargs, self)