def ttl(self, response):
        """Returns time to live in seconds. 0 means no caching.

        Criteria:
        - response code 200
        - read-only method (GET, HEAD, OPTIONS)
        Plus http headers:
        - cache-control: option1, option2, ...
          where options are:
          private | public
          no-cache
          no-store
          max-age: seconds
          s-maxage: seconds
          must-revalidate
          proxy-revalidate
        - expires: Thu, 01 Dec 1983 20:00:00 GMT
        - pragma: no-cache (=cache-control: no-cache)

        See http://www.mobify.com/blog/beginners-guide-to-http-cache-headers/

        TODO: tests

        """
        if response.code != 200: return 0
        if not self.request.method in ['GET', 'HEAD', 'OPTIONS']: return 0

        try:
            pragma = self.request.headers['pragma']
            if pragma == 'no-cache':
                return 0
        except KeyError:
            pass

        try:
            cache_control = self.request.headers['cache-control']

            # no caching options
            for option in ['private', 'no-cache', 'no-store', 'must-revalidate', 'proxy-revalidate']:
                if cache_control.find(option): return 0

            # further parsing to get a ttl
            options = parse_cache_control(cache_control)
            try:
                return int(options['s-maxage'])
            except KeyError:
                pass
            try:
                return int(options['max-age'])
            except KeyError:
                pass

            if 's-maxage' in options:
                max_age = options['s-maxage']
                if max_age < ttl: ttl = max_age
            if 'max-age' in options:
                max_age = options['max-age']
                if max_age < ttl: ttl = max_age
            return ttl
        except KeyError:
            pass

        try:
            expires = self.request.headers['expires']
            return time.mktime(time.strptime(expires, '%a, %d %b %Y %H:%M:%S')) - time.time()
        except KeyError:
            pass