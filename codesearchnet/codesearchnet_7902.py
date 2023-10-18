def process_event(self, packet):
        """This function dispatches ``event`` messages to the correct
        functions. You should override this method only if you are not
        satisfied with the automatic dispatching to
        ``on_``-prefixed methods.  You could then implement your own dispatch.
        See the source code for inspiration.

        There are two ways to deal with callbacks from the client side
        (meaning, the browser has a callback waiting for data that this
        server will be sending back):

        The first one is simply to return an object.  If the incoming
        packet requested has an 'ack' field set, meaning the browser is
        waiting for callback data, it will automatically be packaged
        and sent, associated with the 'ackId' from the browser. The
        return value must be a *sequence* of elements, that will be
        mapped to the positional parameters of the callback function
        on the browser side.

        If you want to *know* that you're dealing with a packet
        that requires a return value, you can do those things manually
        by inspecting the ``ack`` and ``id`` keys from the ``packet``
        object.  Your callback will behave specially if the name of
        the argument to your method is ``packet``.  It will fill it
        with the unprocessed ``packet`` object for your inspection,
        like this:

        .. code-block:: python

          def on_my_callback(self, packet):
              if 'ack' in packet:
                  self.emit('go_back', 'param1', id=packet['id'])
        """
        args = packet['args']
        name = packet['name']
        if not allowed_event_name_regex.match(name):
            self.error("unallowed_event_name",
                       "name must only contains alpha numerical characters")
            return

        method_name = 'on_' + name.replace(' ', '_')
        # This means the args, passed as a list, will be expanded to
        # the method arg and if you passed a dict, it will be a dict
        # as the first parameter.

        return self.call_method_with_acl(method_name, packet, *args)