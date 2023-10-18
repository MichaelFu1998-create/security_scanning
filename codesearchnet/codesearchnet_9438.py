def remove_tweets(self, url):
        """Tries to remove cached tweets."""
        try:
            del self.cache[url]
            self.mark_updated()
            return True
        except KeyError:
            return False