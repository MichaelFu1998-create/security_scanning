def iter_hostnames(self):
        """
        Yields a list of tuples of the form (ip, hostname).
        """
        from burlap.common import get_hosts_retriever
        if self.env.use_retriever:
            self.vprint('using retriever')
            self.vprint('hosts:', self.genv.hosts)
            retriever = get_hosts_retriever()
            hosts = list(retriever(extended=1))
            for _hostname, _data in hosts:

                # Skip hosts that aren't selected for this run.
                if self.genv.hosts \
                and _data.ip not in self.genv.hosts \
                and _data.public_dns_name not in self.genv.hosts \
                and _hostname not in self.genv.hosts:
                    continue

                assert _data.ip, 'Missing IP.'
                yield _data.ip, _hostname#_data.public_dns_name
        else:
            self.vprint('using default')
            for ip, hostname in self.env.hostnames.items():
                self.vprint('ip lookup:', ip, hostname)
                if ip == UNKNOWN:
                    ip = self.hostname_to_ip(hostname)
                    if not ip and hostname in self.env.default_hostnames:
                        ip = self.hostname_to_ip(self.env.default_hostnames[hostname])
                elif not ip[0].isdigit():
                    ip = self.hostname_to_ip(ip)
                assert ip, 'Invalid IP.'
                yield ip, hostname