def emit(self, event, *args, **kwargs):
        """Use this to send a structured event, with a name and arguments, to
        the client.

        By default, it uses this namespace's endpoint. You can send messages on
        other endpoints with something like:

            ``self.socket['/other_endpoint'].emit()``.

        However, it is possible that the ``'/other_endpoint'`` was not
        initialized yet, and that would yield a ``KeyError``.

        The only supported ``kwargs`` is ``callback``.  All other parameters
        must be passed positionally.

        :param event: The name of the event to trigger on the other end.
        :param callback: Pass in the callback keyword argument to define a
                         call-back that will be called when the client acks.

                         This callback is slightly different from the one from
                         ``send()``, as this callback will receive parameters
                         from the explicit call of the ``ack()`` function
                         passed to the listener on the client side.

                         The remote listener will need to explicitly ack (by
                         calling its last argument, a function which is
                         usually called 'ack') with some parameters indicating
                         success or error.  The 'ack' packet coming back here
                         will then trigger the callback function with the
                         returned values.
        :type callback: callable
        """
        callback = kwargs.pop('callback', None)

        if kwargs:
            raise ValueError(
                "emit() only supports positional argument, to stay "
                "compatible with the Socket.IO protocol. You can "
                "however pass in a dictionary as the first argument")
        pkt = dict(type="event", name=event, args=args,
                   endpoint=self.ns_name)

        if callback:
            # By passing 'data', we indicate that we *want* an explicit ack
            # by the client code, not an automatic as with send().
            pkt['ack'] = 'data'
            pkt['id'] = msgid = self.socket._get_next_msgid()
            self.socket._save_ack_callback(msgid, callback)

        self.socket.send_packet(pkt)