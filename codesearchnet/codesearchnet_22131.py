def update(self, server):
        """Update existing challenge on the server"""

        return server.put(
            'challenge_admin',
            self.as_payload(),
            replacements={'slug': self.slug})