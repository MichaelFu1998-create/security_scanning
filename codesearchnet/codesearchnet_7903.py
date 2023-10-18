def call_method_with_acl(self, method_name, packet, *args):
        """You should always use this function to call the methods,
        as it checks if the user is allowed according to the ACLs.

        If you override :meth:`process_packet` or
        :meth:`process_event`, you should definitely want to use this
        instead of ``getattr(self, 'my_method')()``
        """
        if not self.is_method_allowed(method_name):
            self.error('method_access_denied',
                       'You do not have access to method "%s"' % method_name)
            return

        return self.call_method(method_name, packet, *args)