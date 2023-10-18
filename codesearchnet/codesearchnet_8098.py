def _follow_next(self, url):
        """Follow the 'next' link on paginated results."""
        response = self._json(self._get(url), 200)
        data = response['data']

        next_url = self._get_attribute(response, 'links', 'next')
        while next_url is not None:
            response = self._json(self._get(next_url), 200)
            data.extend(response['data'])
            next_url = self._get_attribute(response, 'links', 'next')

        return data