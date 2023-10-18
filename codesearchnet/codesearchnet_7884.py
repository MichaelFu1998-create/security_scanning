def kill(self, detach=False):
        """This function must/will be called when a socket is to be completely
        shut down, closed by connection timeout, connection error or explicit
        disconnection from the client.

        It will call all of the Namespace's
        :meth:`~socketio.namespace.BaseNamespace.disconnect` methods
        so that you can shut-down things properly.

        """
        # Clear out the callbacks
        self.ack_callbacks = {}
        if self.connected:
            self.state = self.STATE_DISCONNECTING
            self.server_queue.put_nowait(None)
            self.client_queue.put_nowait(None)
            if len(self.active_ns) > 0:
                log.debug("Calling disconnect() on %s" % self)
                self.disconnect()

        if detach:
            self.detach()

        gevent.killall(self.jobs)