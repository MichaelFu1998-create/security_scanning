def seed_url(self):
        """A URL that can be used to open the page.

        The URL is formatted from :py:attr:`URL_TEMPLATE`, which is then
        appended to :py:attr:`base_url` unless the template results in an
        absolute URL.

        :return: URL that can be used to open the page.
        :rtype: str

        """
        url = self.base_url
        if self.URL_TEMPLATE is not None:
            url = urlparse.urljoin(
                self.base_url, self.URL_TEMPLATE.format(**self.url_kwargs)
            )

        if not url:
            return None

        url_parts = list(urlparse.urlparse(url))
        query = urlparse.parse_qsl(url_parts[4])

        for k, v in self.url_kwargs.items():
            if v is None:
                continue
            if "{{{}}}".format(k) not in str(self.URL_TEMPLATE):
                for i in iterable(v):
                    query.append((k, i))

        url_parts[4] = urlencode(query)
        return urlparse.urlunparse(url_parts)