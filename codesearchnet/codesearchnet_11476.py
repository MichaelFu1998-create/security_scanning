def connect(self, host):
        """
            Connect to a host
        """
        if not self.app.connect(host):
            command = "Connect({0})".format(host).encode("ascii")
            self.exec_command(command)
        self.last_host = host