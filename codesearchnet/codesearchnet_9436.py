def add_tweets(self, url, last_modified, tweets):
        """Adds new tweets to the cache."""
        try:
            self.cache[url] = {"last_modified": last_modified, "tweets": tweets}
            self.mark_updated()
            return True
        except TypeError:
            return False