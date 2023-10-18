def url(self, url, encoding="UTF-8"):
        """load and process the content behind a url

        :return: the processed result of the :paramref:`url's <url>` content
        :param str url: the url to retrieve the content from
        :param str encoding: the encoding of the retrieved content.
          The default encoding is UTF-8.

        """
        import urllib.request
        with urllib.request.urlopen(url) as file:
            webpage_content = file.read()
        webpage_content = webpage_content.decode(encoding)
        return self.string(webpage_content)