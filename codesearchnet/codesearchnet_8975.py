def auto_client(cls, host, server, ca_path=None, ca_contents=None,
                    cert_path=None, cert_contents=None, key_path=None,
                    key_contents=None):
        """
        Returns a configuration dictionary representing an OpenVPN client configuration
        that is compatible with the passed server configuration.

        :param host: remote VPN server
        :param server: dictionary representing a single OpenVPN server configuration
        :param ca_path: optional string representing path to CA, will consequently add
                        a file in the resulting configuration dictionary
        :param ca_contents: optional string representing contents of CA file
        :param cert_path: optional string representing path to certificate, will consequently add
                        a file in the resulting configuration dictionary
        :param cert_contents: optional string representing contents of cert file
        :param key_path: optional string representing path to key, will consequently add
                        a file in the resulting configuration dictionary
        :param key_contents: optional string representing contents of key file
        :returns: dictionary representing a single OpenVPN client configuration
        """
        # client defaults
        client = {
            "mode": "p2p",
            "nobind": True,
            "resolv_retry": "infinite",
            "tls_client": True
        }
        # remote
        port = server.get('port') or 1195
        client['remote'] = [{'host': host, 'port': port}]
        # proto
        if server.get('proto') == 'tcp-server':
            client['proto'] = 'tcp-client'
        else:
            client['proto'] = 'udp'
        # determine if pull must be True
        if 'server' in server or 'server_bridge' in server:
            client['pull'] = True
        # tls_client
        if 'tls_server' not in server or not server['tls_server']:
            client['tls_client'] = False
        # ns_cert_type
        ns_cert_type = {None: '',
                        '': '',
                        'client': 'server'}
        client['ns_cert_type'] = ns_cert_type[server.get('ns_cert_type')]
        # remote_cert_tls
        remote_cert_tls = {None: '',
                           '': '',
                           'client': 'server'}
        client['remote_cert_tls'] = remote_cert_tls[server.get('remote_cert_tls')]
        copy_keys = ['name', 'dev_type', 'dev', 'comp_lzo', 'auth',
                     'cipher', 'ca', 'cert', 'key', 'pkcs12', 'mtu_disc', 'mtu_test',
                     'fragment', 'mssfix', 'keepalive', 'persist_tun', 'mute',
                     'persist_key', 'script_security', 'user', 'group', 'log',
                     'mute_replay_warnings', 'secret', 'reneg_sec', 'tls_timeout',
                     'tls_cipher', 'float', 'fast_io', 'verb']
        for key in copy_keys:
            if key in server:
                client[key] = server[key]
        files = cls._auto_client_files(client, ca_path, ca_contents,
                                       cert_path, cert_contents,
                                       key_path, key_contents)
        return {
            'openvpn': [client],
            'files': files
        }