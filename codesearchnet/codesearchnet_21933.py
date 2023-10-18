def cache_get(self):
        "Returns (headers, body) from the cache or raise KeyError"
        key = self.cache_key()
        (headers, body, expires_ts) = self.application._cache[key]
        if expires_ts < time.now():
            # asset has expired, delete it
            del self.application._cache[key]
            raise KeyError(key)

        return (headers, body)