def _resolve_hostname(self):
        """Start hostname resolution for the next name to try.

        [called with `lock` acquired]
        """
        self._set_state("resolving-hostname")
        resolver = self.settings["dns_resolver"] # pylint: disable=W0621
        logger.debug("_dst_nameports: {0!r}".format(self._dst_nameports))
        name, port = self._dst_nameports.pop(0)
        self._dst_hostname = name
        resolver.resolve_address(name, callback = partial(
                                self._got_addresses, name, port),
                                allow_cname = self._dst_service is None)
        self.event(ResolvingAddressEvent(name))