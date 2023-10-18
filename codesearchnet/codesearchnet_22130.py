def create(self, server):
        """Create the challenge on the server"""

        return server.post(
            'challenge_admin',
            self.as_payload(),
            replacements={'slug': self.slug})