def call_method(self, method_name, packet, *args):
        """This function is used to implement the two behaviors on dispatched
        ``on_*()`` and ``recv_*()`` method calls.

        Those are the two behaviors:

        * If there is only one parameter on the dispatched method and
          it is named ``packet``, then pass in the packet dict as the
          sole parameter.

        * Otherwise, pass in the arguments as specified by the
          different ``recv_*()`` methods args specs, or the
          :meth:`process_event` documentation.

        This method will also consider the
        ``exception_handler_decorator``.  See Namespace documentation
        for details and examples.

        """
        method = getattr(self, method_name, None)
        if method is None:
            self.error('no_such_method',
                       'The method "%s" was not found' % method_name)
            return

        specs = inspect.getargspec(method)
        func_args = specs.args
        if not len(func_args) or func_args[0] != 'self':
            self.error("invalid_method_args",
                "The server-side method is invalid, as it doesn't "
                "have 'self' as its first argument")
            return

        # Check if we need to decorate to handle exceptions
        if hasattr(self, 'exception_handler_decorator'):
            method = self.exception_handler_decorator(method)

        if len(func_args) == 2 and func_args[1] == 'packet':
            return method(packet)
        else:
            return method(*args)