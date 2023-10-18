def _makeInstance(self, clazz, args, kwargs):
        '''Creates an instance of a class defined in this document.
           This method sets the context of the object to the current context.'''
        inst = clazz(self, *args, **kwargs)
        return inst