def exists(self, server):
        """Check if a challenge exists on the server"""

        try:
            server.get(
                'challenge',
                replacements={'slug': self.slug})
        except Exception:
            return False
        return True