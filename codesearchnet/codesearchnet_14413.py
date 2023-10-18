def init(self, hosts=None, cacert=None, client_cert=None, client_key=None):
        """
        Handle creating the new etcd client instance and other business.

        :param hosts: Host string or list of hosts (default: `'127.0.0.1:2379'`)
        :param cacert: CA cert filename (optional)
        :param client_cert: Client cert filename (optional)
        :param client_key: Client key filename (optional)
        :type ca: str
        :type cert: str
        :type key: str

        """
        # Try to get the etcd module
        try:
            import etcd
            self.module = etcd
        except ImportError:
            pass

        if not self.module:
            return

        self._parse_jetconfig()

        # Check env for overriding configuration or pyconfig setting
        hosts = env('PYCONFIG_ETCD_HOSTS', hosts)
        protocol = env('PYCONFIG_ETCD_PROTOCOL', None)
        cacert = env('PYCONFIG_ETCD_CACERT', cacert)
        client_cert = env('PYCONFIG_ETCD_CERT', client_cert)
        client_key = env('PYCONFIG_ETCD_KEY', client_key)

        # Parse auth string if there is one
        username = None
        password = None
        auth = env('PYCONFIG_ETCD_AUTH', None)
        if auth:
            auth = auth.split(':')
            auth.append('')
            username = auth[0]
            password = auth[1]

        # Create new etcd instance
        hosts = self._parse_hosts(hosts)
        if hosts is None:
            return

        kw = {}
        # Need this when passing a list of hosts to python-etcd, which we
        # always do, even if it's a list of one
        kw['allow_reconnect'] = True

        # Grab optional protocol argument
        if protocol:
            kw['protocol'] = protocol

        # Add auth to constructor if we got it
        if username:
            kw['username'] = username
        if password:
            kw['password'] = password

        # Assign the SSL args if we have 'em
        if cacert:
            kw['ca_cert'] = os.path.abspath(cacert)
        if client_cert and client_key:
            kw['cert'] = ((os.path.abspath(client_cert),
                os.path.abspath(client_key)))
        elif client_cert:
            kw['cert'] = os.path.abspath(client_cert)
        if cacert or client_cert or client_key:
            kw['protocol'] = 'https'

        self.client = self.module.Client(hosts, **kw)