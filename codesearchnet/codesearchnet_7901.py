def process_packet(self, packet):
        """If you override this, NONE of the functions in this class
        will be called.  It is responsible for dispatching to
        :meth:`process_event` (which in turn calls ``on_*()`` and
        ``recv_*()`` methods).

        If the packet arrived here, it is because it belongs to this endpoint.

        For each packet arriving, the only possible path of execution, that is,
        the only methods that *can* be called are the following:

        * recv_connect()
        * recv_message()
        * recv_json()
        * recv_error()
        * recv_disconnect()
        * on_*()
        """
        packet_type = packet['type']

        if packet_type == 'event':
            return self.process_event(packet)
        elif packet_type == 'message':
            return self.call_method_with_acl('recv_message', packet,
                                             packet['data'])
        elif packet_type == 'json':
            return self.call_method_with_acl('recv_json', packet,
                                             packet['data'])
        elif packet_type == 'connect':
            self.socket.send_packet(packet)
            return self.call_method_with_acl('recv_connect', packet)
        elif packet_type == 'error':
            return self.call_method_with_acl('recv_error', packet)
        elif packet_type == 'ack':
            callback = self.socket._pop_ack_callback(packet['ackId'])
            if not callback:
                print("ERROR: No such callback for ackId %s" % packet['ackId'])
                return
            return callback(*(packet['args']))
        elif packet_type == 'disconnect':
            # Force a disconnect on the namespace.
            return self.call_method_with_acl('recv_disconnect', packet)
        else:
            print("Unprocessed packet", packet)