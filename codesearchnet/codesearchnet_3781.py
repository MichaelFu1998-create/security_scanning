def get_prefix(self, include_version=True):
        """Return the appropriate URL prefix to prepend to requests,
        based on the host provided in settings.
        """
        host = settings.host
        if '://' not in host:
            host = 'https://%s' % host.strip('/')
        elif host.startswith('http://') and settings.verify_ssl:
            raise exc.TowerCLIError(
                'Can not verify ssl with non-https protocol. Change the '
                'verify_ssl configuration setting to continue.'
            )
        # Validate that we have either an http or https based URL
        url_pieces = urlparse(host)
        if url_pieces[0] not in ['http', 'https']:
            raise exc.ConnectionError('URL must be http(s), {} is not valid'.format(url_pieces[0]))

        prefix = urljoin(host, '/api/')
        if include_version:
            # We add the / to the end of {} so that our URL has the ending slash.
            prefix = urljoin(prefix, "{}/".format(CUR_API_VERSION))

        return prefix