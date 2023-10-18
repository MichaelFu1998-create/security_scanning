def available(self, timeout=5):
        """Returns True if database server is running, False otherwise."""
        host = self._connect_args['host']
        port = self._connect_args['port']
        try:
            sock = socket.create_connection((host, port), timeout=timeout)
            sock.close()
            return True
        except socket.error:
            pass
        return False