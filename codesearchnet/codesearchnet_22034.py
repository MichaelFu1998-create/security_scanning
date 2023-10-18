def authorize(self):
        """Authenticates the superuser account via the web login."""
        response = self.client.login(username=self.USERNAME, 
            password=self.PASSWORD)
        self.assertTrue(response)
        self.authed = True