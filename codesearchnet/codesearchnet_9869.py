def raw_iter(self, stream=False):
        """https://github.com/frictionlessdata/datapackage-py#resource
        """

        # Error for inline
        if self.inline:
            message = 'Methods raw_iter/raw_read are not supported for inline data'
            raise exceptions.DataPackageException(message)

        # Get filelike
        if self.multipart:
            filelike = _MultipartSource(self.source, remote=self.remote)
        elif self.remote:
            if self.__table_options.get('http_session'):
                http_session = self.__table_options['http_session']
            else:
                http_session = requests.Session()
                http_session.headers = config.HTTP_HEADERS
            res = http_session.get(self.source, stream=True)
            filelike = res.raw
        else:
            filelike = io.open(self.source, 'rb')

        return filelike