def _got_addresses(self, name, port, addrs):
        """Handler DNS address record lookup result.

        :Parameters:
            - `name`: the name requested
            - `port`: port number to connect to
            - `addrs`: list of (family, address) tuples
        """
        with self.lock:
            if not addrs:
                if self._dst_nameports:
                    self._set_state("resolve-hostname")
                    return
                else:
                    self._dst_addrs = []
                    self._set_state("aborted")
                    raise DNSError("Could not resolve address record for {0!r}"
                                                                .format(name))
            self._dst_addrs = [ (family, (addr, port)) for (family, addr)
                                                                    in addrs ]
            self._set_state("connect")