def retrieve_url(self, url):
        """
        Use requests to fetch remote content
        """

        try:
            r = requests.get(url)
        except requests.ConnectionError:
            raise exceptions.RetrieveError('Connection fail')

        if r.status_code >= 400:
            raise exceptions.RetrieveError('Connected, but status code is %s' % (r.status_code))

        real_url = r.url
        content = r.content

        try:
            content_type = r.headers['Content-Type']
        except KeyError:
            content_type, encoding = mimetypes.guess_type(real_url, strict=False)

        self.response = r

        return content_type.lower(), content