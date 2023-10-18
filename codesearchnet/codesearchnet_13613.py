def _got_srv(self, addrs):
        """Handle SRV lookup result.

        :Parameters:
            - `addrs`: properly sorted list of (hostname, port) tuples
        """
        with self.lock:
            if not addrs:
                self._dst_service = None
                if self._dst_port:
                    self._dst_nameports = [(self._dst_name, self._dst_port)]
                else:
                    self._dst_nameports = []
                    self._set_state("aborted")
                    raise DNSError("Could not resolve SRV for service {0!r}"
                            " on host {1!r} and fallback port number not given"
                                    .format(self._dst_service, self._dst_name))
            elif addrs == [(".", 0)]:
                self._dst_nameports = []
                self._set_state("aborted")
                raise DNSError("Service {0!r} not available on host {1!r}"
                                    .format(self._dst_service, self._dst_name))
            else:
                self._dst_nameports = addrs
            self._set_state("resolve-hostname")