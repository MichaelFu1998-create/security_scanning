def begin(self):
        """ connects and optionally authenticates a connection."""
        self.connect(self.host, self.port)
        if self.user:
            self.starttls()
            self.login(self.user, self.password)