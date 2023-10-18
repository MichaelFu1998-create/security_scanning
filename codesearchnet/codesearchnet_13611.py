def _connect(self, addr, port, service):
        """Same as `connect`, but assumes `lock` acquired.
        """
        self._dst_name = addr
        self._dst_port = port
        family = None
        try:
            res = socket.getaddrinfo(addr, port, socket.AF_UNSPEC,
                                socket.SOCK_STREAM, 0, socket.AI_NUMERICHOST)
            family = res[0][0]
            sockaddr = res[0][4]
        except socket.gaierror:
            family = None
            sockaddr = None

        if family is not None:
            if not port:
                raise ValueError("No port number given with literal IP address")
            self._dst_service = None
            self._family = family
            self._dst_addrs = [(family, sockaddr)]
            self._set_state("connect")
        elif service is not None:
            self._dst_service = service
            self._set_state("resolve-srv")
            self._dst_name = addr
        elif port:
            self._dst_nameports = [(self._dst_name, self._dst_port)]
            self._dst_service = None
            self._set_state("resolve-hostname")
        else:
            raise ValueError("No port number and no SRV service name given")