def saveSession(self):
        """Save cookies/session."""
        if self.cookies_file:
            self.r.cookies.save(ignore_discard=True)
            with open(self.token_file, 'w') as f:
                f.write('%s %s' % (self.token_type, self.access_token))