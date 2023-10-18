def open_socket(self):
        """
        Opens the socket and binds to the given host and port. Uses
        SO_REUSEADDR to be as robust as possible.
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setblocking(0)
        self.socket.bind((self.host, self.port))