def is_cached(self, url):
        """Checks if specified URL is cached."""
        try:
            return True if url in self.cache else False
        except TypeError:
            return False