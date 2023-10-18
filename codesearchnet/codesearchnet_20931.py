def cookies(self):
        """Request cookies

        :rtype: dict
        """
        http_cookie = self.environ.get('HTTP_COOKIE', '')
        _cookies = {
            k: v.value
            for (k, v) in SimpleCookie(http_cookie).items()
        }
        return _cookies