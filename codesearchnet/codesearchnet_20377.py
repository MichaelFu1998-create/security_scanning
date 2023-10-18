def gen_methods(self, *args, **kwargs):
        '''Find all method names this input dispatches to. This method
        can accept *args, **kwargs, but it's the gen_dispatch method's
        job of passing specific args to handler methods.
        '''
        dispatched = False
        for invoc, methodname in self.registry:
            args, kwargs = self.loads(invoc)
            yield getattr(self.inst, methodname), args, kwargs
            dispatched = True

        if dispatched:
            return

        # Try the generic handler.
        generic_handler = getattr(self.inst, 'generic_handler', None)
        if generic_handler is not None:
            yield generic_handler, args, kwargs

        # Give up.
        msg = 'No method was found for %r on %r.'
        raise self.DispatchError(msg % ((args, kwargs), self.inst))