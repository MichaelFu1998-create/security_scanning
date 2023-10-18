def _waitFor(self, timeout, notification, **kwargs):
        """Wait for a particular UI event to occur; this can be built
        upon in NativeUIElement for specific convenience methods.
        """
        callback = self._matchOther
        retelem = None
        callbackArgs = None
        callbackKwargs = None

        # Allow customization of the callback, though by default use the basic
        # _match() method
        if 'callback' in kwargs:
            callback = kwargs['callback']
            del kwargs['callback']

            # Deal with these only if callback is provided:
            if 'args' in kwargs:
                if not isinstance(kwargs['args'], tuple):
                    errStr = 'Notification callback args not given as a tuple'
                    raise TypeError(errStr)

                # If args are given, notification will pass back the returned
                # element in the first positional arg
                callbackArgs = kwargs['args']
                del kwargs['args']

            if 'kwargs' in kwargs:
                if not isinstance(kwargs['kwargs'], dict):
                    errStr = 'Notification callback kwargs not given as a dict'
                    raise TypeError(errStr)

                callbackKwargs = kwargs['kwargs']
                del kwargs['kwargs']
            # If kwargs are not given as a dictionary but individually listed
            # need to update the callbackKwargs dict with the remaining items in
            # kwargs
            if kwargs:
                if callbackKwargs:
                    callbackKwargs.update(kwargs)
                else:
                    callbackKwargs = kwargs
        else:
            callbackArgs = (retelem,)
            # Pass the kwargs to the default callback
            callbackKwargs = kwargs

        return self._setNotification(timeout, notification, callback,
                                     callbackArgs,
                                     callbackKwargs)