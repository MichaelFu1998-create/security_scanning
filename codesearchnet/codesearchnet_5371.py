def emit(self, *args, **kwargs):
        """
        Emits the signal, passing the given arguments to the callbacks.
        If one of the callbacks returns a value other than None, no further
        callbacks are invoked and the return value of the callback is
        returned to the caller of emit().

        :type  args: tuple
        :param args: Optional arguments passed to the callbacks.
        :type  kwargs: dict
        :param kwargs: Optional keyword arguments passed to the callbacks.
        :rtype:  object
        :returns: Returns None if all callbacks returned None. Returns
                 the return value of the last invoked callback otherwise.
        """
        if self.hard_subscribers is not None:
            for callback, user_args, user_kwargs in self.hard_subscribers:
                kwargs.update(user_kwargs)
                result = callback(*args + user_args, **kwargs)
                if result is not None:
                    return result

        if self.weak_subscribers is not None:
            for callback, user_args, user_kwargs in self.weak_subscribers:
                kwargs.update(user_kwargs)

                # Even though WeakMethod notifies us when the underlying
                # function is destroyed, and we remove the item from the
                # the list of subscribers, there is no guarantee that
                # this notification has already happened because the garbage
                # collector may run while this loop is executed.
                # Disabling the garbage collector temporarily also does
                # not work, because other threads may be trying to do
                # the same, causing yet another race condition.
                # So the only solution is to skip such functions.
                function = callback.get_function()
                if function is None:
                    continue
                result = function(*args + user_args, **kwargs)
                if result is not None:
                    return result