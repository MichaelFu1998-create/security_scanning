def login(self, username, password=None, token=None):
        """Login user for protected API calls."""
        self.session.basic_auth(username, password)