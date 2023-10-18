def _parse_jetconfig(self):
        """
        Undocumented cross-compatability functionality with jetconfig
        (https://github.com/shakefu/jetconfig) that is very sloppy.

        """
        conf = env('JETCONFIG_ETCD', None)

        if not conf:
            return

        import urlparse

        auth = None
        port = None
        conf = conf.split(',').pop()
        entry = urlparse.urlparse(conf)
        scheme = entry.scheme
        host = entry.netloc or entry.path # Path is where it goes if there's no
                                          # scheme on the URL

        if '@' in host:
            auth, host = host.split('@')

        if ':' in host:
            host, port = host.split(':')

        if not port and scheme == 'https':
            port = '443'

        if scheme:
            os.environ['PYCONFIG_ETCD_PROTOCOL'] = scheme

        if auth:
            os.environ['PYCONFIG_ETCD_AUTH'] = auth

        if port:
            host = host + ":" + port

        os.environ['PYCONFIG_ETCD_HOSTS'] = host