def is_connected(self):
        """
            Return bool indicating connection state
        """
        # need to wrap in try/except b/c of wc3270's socket connection dynamics
        try:
            # this is basically a no-op, but it results in the the current status
            # getting updated
            self.exec_command(b"Query(ConnectionState)")

            # connected status is like 'C(192.168.1.1)', disconnected is 'N'
            return self.status.connection_state.startswith(b"C(")
        except NotConnectedException:
            return False