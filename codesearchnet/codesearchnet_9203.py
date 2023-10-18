def __check_looks_like_uri(self, uri):
        """Checks the URI looks like a RAW uri in github:

        - 'https://raw.githubusercontent.com/github/hubot/master/README.md'
        - 'https://github.com/github/hubot/raw/master/README.md'

        :param uri: uri of the file
        """
        if uri.split('/')[2] == 'raw.githubusercontent.com':
            return True
        elif uri.split('/')[2] == 'github.com':
            if uri.split('/')[5] == 'raw':
                return True
        else:
            raise GithubFileNotFound('URI %s is not a valid link to a raw file in Github' % uri)