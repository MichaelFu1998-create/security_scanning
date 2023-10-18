def disconnect(self, silent=False):
        """Calling this method will call the
        :meth:`~socketio.namespace.BaseNamespace.disconnect` method on
        all the active Namespaces that were open, killing all their
        jobs and sending 'disconnect' packets for each of them.

        Normally, the Global namespace (endpoint = '') has special meaning,
        as it represents the whole connection,

        :param silent: when True, pass on the ``silent`` flag to the Namespace
                       :meth:`~socketio.namespace.BaseNamespace.disconnect`
                       calls.
        """
        for ns_name, ns in list(six.iteritems(self.active_ns)):
            ns.recv_disconnect()