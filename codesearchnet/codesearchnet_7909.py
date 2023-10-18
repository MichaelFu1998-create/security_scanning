def disconnect(self, silent=False):
        """Send a 'disconnect' packet, so that the user knows it has been
        disconnected (booted actually).  This will trigger an onDisconnect()
        call on the client side.

        Over here, we will kill all ``spawn``ed processes and remove the
        namespace from the Socket object.

        :param silent: do not actually send the packet (if they asked for a
                       disconnect for example), but just kill all jobs spawned
                       by this Namespace, and remove it from the Socket.
        """
        if not silent:
            packet = {"type": "disconnect",
                      "endpoint": self.ns_name}
            self.socket.send_packet(packet)
        # remove_namespace might throw GreenletExit so
        # kill_local_jobs must be in finally
        try:
            self.socket.remove_namespace(self.ns_name)
        finally:
            self.kill_local_jobs()