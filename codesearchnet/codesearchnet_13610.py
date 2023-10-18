def connect(self, addr, port = None, service = None):
        """Start establishing TCP connection with given address.

        One of: `port` or `service` must be provided and `addr` must be
        a domain name and not an IP address if `port` is not given.

        When `service` is given try an SRV lookup for that service
        at domain `addr`. If `service` is not given or `addr` is an IP address,
        or the SRV lookup fails, connect to `port` at host `addr` directly.

        [initiating entity only]

        :Parameters:
            - `addr`: peer name or IP address
            - `port`: port number to connect to
            - `service`: service name (to be resolved using SRV DNS records)
        """
        with self.lock:
            self._connect(addr, port, service)