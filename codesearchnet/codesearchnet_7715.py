def _gethostbyname(self, hostname):
        """
        Hostname lookup method, supports both IPv4 and IPv6.
        """
        if self._databaseType in const.IPV6_EDITIONS:
            response = socket.getaddrinfo(hostname, 0, socket.AF_INET6)
            family, socktype, proto, canonname, sockaddr = response[0]
            address, port, flow, scope = sockaddr
            return address
        else:
            return socket.gethostbyname(hostname)