def _receiver_loop(self):
        """This is the loop that takes messages from the queue for the server
        to consume, decodes them and dispatches them.

        It is the main loop for a socket.  We join on this process before
        returning control to the web framework.

        This process is not tracked by the socket itself, it is not going
        to be killed by the ``gevent.killall(socket.jobs)``, so it must
        exit gracefully itself.
        """

        while True:
            rawdata = self.get_server_msg()

            if not rawdata:
                continue  # or close the connection ?
            try:
                pkt = packet.decode(rawdata, self.json_loads)
            except (ValueError, KeyError, Exception) as e:
                self.error('invalid_packet',
                    "There was a decoding error when dealing with packet "
                    "with event: %s... (%s)" % (rawdata[:20], e))
                continue

            if pkt['type'] == 'heartbeat':
                # This is already dealth with in put_server_msg() when
                # any incoming raw data arrives.
                continue

            if pkt['type'] == 'disconnect' and pkt['endpoint'] == '':
                # On global namespace, we kill everything.
                self.kill(detach=True)
                continue

            endpoint = pkt['endpoint']

            if endpoint not in self.namespaces:
                self.error("no_such_namespace",
                    "The endpoint you tried to connect to "
                    "doesn't exist: %s" % endpoint, endpoint=endpoint)
                continue
            elif endpoint in self.active_ns:
                pkt_ns = self.active_ns[endpoint]
            else:
                new_ns_class = self.namespaces[endpoint]
                pkt_ns = new_ns_class(self.environ, endpoint,
                                        request=self.request)
                # This calls initialize() on all the classes and mixins, etc..
                # in the order of the MRO
                for cls in type(pkt_ns).__mro__:
                    if hasattr(cls, 'initialize'):
                        cls.initialize(pkt_ns)  # use this instead of __init__,
                                                # for less confusion

                self.active_ns[endpoint] = pkt_ns

            retval = pkt_ns.process_packet(pkt)

            # Has the client requested an 'ack' with the reply parameters ?
            if pkt.get('ack') == "data" and pkt.get('id'):
                if type(retval) is tuple:
                    args = list(retval)
                else:
                    args = [retval]
                returning_ack = dict(type='ack', ackId=pkt['id'],
                                     args=args,
                                     endpoint=pkt.get('endpoint', ''))
                self.send_packet(returning_ack)

            # Now, are we still connected ?
            if not self.connected:
                self.kill(detach=True)  # ?? what,s the best clean-up
                                        # when its not a
                                        # user-initiated disconnect
                return