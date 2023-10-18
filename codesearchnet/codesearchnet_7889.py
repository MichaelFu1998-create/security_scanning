def remove_namespace(self, namespace):
        """This removes a Namespace object from the socket.

        This is usually called by
        :meth:`~socketio.namespace.BaseNamespace.disconnect`.

        """
        if namespace in self.active_ns:
            del self.active_ns[namespace]

        if len(self.active_ns) == 0 and self.connected:
            self.kill(detach=True)