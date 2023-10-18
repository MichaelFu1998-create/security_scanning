def _bind_args(sig, param_matchers, args, kwargs):
        '''
        Attempt to bind the args to the type signature. First try to just bind
        to the signature, then ensure that all arguments match the parameter
        types.
        '''
        #Bind to signature. May throw its own TypeError
        bound = sig.bind(*args, **kwargs)

        if not all(param_matcher(bound.arguments[param_name])
                for param_name, param_matcher in param_matchers):
            raise TypeError

        return bound