def _parse_hosts(self, hosts):
        """
        Return hosts parsed into a tuple of tuples.

        :param hosts: String or list of hosts

        """
        # Default host
        if hosts is None:
            return

        # If it's a string, we allow comma separated strings
        if isinstance(hosts, six.string_types):
            # Split comma-separated list
            hosts = [host.strip() for host in hosts.split(',')]
            # Split host and port
            hosts = [host.split(':') for host in hosts]
            # Coerce ports to int
            hosts = [(host[0], int(host[1])) for host in hosts]

        # The python-etcd client explicitly checks for a tuple type
        return tuple(hosts)