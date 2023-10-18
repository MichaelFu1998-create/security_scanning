def _user_headers(self, headers=None):
        """ Make sure the user doesn't override the Authorization header """
        h = self.copy()

        if headers is not None:
            keys = set(headers.keys())
            if h.get('Authorization', False):
                keys -= {'Authorization'}

            for key in keys:
                h[key] = headers[key]

        return h