def get_tweets(self, url, limit=None):
        """Retrieves tweets from the cache."""
        try:
            tweets = self.cache[url]["tweets"]
            self.mark_updated()
            return sorted(tweets, reverse=True)[:limit]
        except KeyError:
            return []