def _resolve_srv(self):
        """Start resolving the SRV record.
        """
        resolver = self.settings["dns_resolver"] # pylint: disable=W0621
        self._set_state("resolving-srv")
        self.event(ResolvingSRVEvent(self._dst_name, self._dst_service))
        resolver.resolve_srv(self._dst_name, self._dst_service, "tcp",
                                                    callback = self._got_srv)