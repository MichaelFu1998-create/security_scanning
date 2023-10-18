def watch_method(self, method_name, callback):
        """
        Register the given callback to be called whenever the method with the 
        given name is called.  You can easily take advantage of this feature in 
        token extensions by using the @watch_token decorator.
        """

        # Make sure a token method with the given name exists, and complain if 
        # nothing is found.

        try:
            method = getattr(self, method_name)
        except AttributeError:
            raise ApiUsageError("""\
                    {self.__class__.__name__} has no such method 
                    {method_name}() to watch.

                    This error usually means that you used the @watch_token 
                    decorator on a method of a token extension class that 
                    didn't match the name of any method in the corresponding 
                    token class.  Check for typos.""")

        # Wrap the method in a WatchedMethod object, if that hasn't already 
        # been done.  This object manages a list of callback method and takes 
        # responsibility for calling them after the method itself has been 
        # called.

        if not isinstance(method, Token.WatchedMethod):
            setattr(self, method_name, Token.WatchedMethod(method))
            method = getattr(self, method_name)

        # Add the given callback to the watched method.

        method.add_watcher(callback)