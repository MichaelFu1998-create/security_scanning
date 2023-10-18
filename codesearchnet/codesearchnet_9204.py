def read_file_from_uri(self, uri):
        """Reads the file from Github

        :param uri: URI of the Github raw File

        :returns: UTF-8 text with the content
        """
        logger.debug("Reading %s" % (uri))

        self.__check_looks_like_uri(uri)

        try:
            req = urllib.request.Request(uri)
            req.add_header('Authorization', 'token %s' % self.token)
            r = urllib.request.urlopen(req)
        except urllib.error.HTTPError as err:
            if err.code == 404:
                raise GithubFileNotFound('File %s is not available. Check the URL to ensure it really exists' % uri)
            else:
                raise

        return r.read().decode("utf-8")