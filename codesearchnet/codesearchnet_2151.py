def connect(self, timeout=600):
        """
        Starts the server tcp connection on the given host:port.

        Args:
            timeout (int): The time (in seconds) for which we will attempt a connection to the remote
                (every 5sec). After that (or if timeout is None or 0), an error is raised.
        """
        # If we are already connected, return error.
        if self.socket:
            raise TensorForceError("Already connected to {}:{}. Only one connection allowed at a time. " +
                                   "Close first by calling `close`!".format(self.host, self.port))
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if timeout < 5 or timeout is None:
            timeout = 5

        err = 0
        start_time = time.time()
        while time.time() - start_time < timeout:
            self.socket.settimeout(5)
            err = self.socket.connect_ex((self.host, self.port))
            if err == 0:
                break
            time.sleep(1)
        if err != 0:
            raise TensorForceError("Error when trying to connect to {}:{}: errno={} errcode='{}' '{}'".
                                   format(self.host, self.port, err, errno.errorcode[err], os.strerror(err)))