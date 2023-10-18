def resolve_address(self, hostname, callback, allow_cname = True):
        """Start looking up an A or AAAA record.

        `callback` will be called with a list of (family, address) tuples
        on success. Family is :std:`socket.AF_INET` or :std:`socket.AF_INET6`,
        the address is IPv4 or IPv6 literal. The list will be empty on error.

        :Parameters:
            - `hostname`: the host name to look up
            - `callback`: a function to be called with a list of received
              addresses
            - `allow_cname`: `True` if CNAMEs should be followed
        :Types:
            - `hostname`: `unicode`
            - `callback`: function accepting a single argument
            - `allow_cname`: `bool`
        """
        if self.settings["ipv6"]:
            if self.settings["ipv4"]:
                family = socket.AF_UNSPEC
            else:
                family = socket.AF_INET6
        elif self.settings["ipv4"]:
            family = socket.AF_INET
        else:
            logger.warning("Neither IPv6 or IPv4 allowed.")
            callback([])
            return
        try:
            ret = socket.getaddrinfo(hostname, 0, family, socket.SOCK_STREAM, 0)
        except socket.gaierror, err:
            logger.warning("Couldn't resolve {0!r}: {1}".format(hostname,
                                                                        err))
            callback([])
            return
        except IOError as err:
            logger.warning("Couldn't resolve {0!r}, unexpected error: {1}"
                                                        .format(hostname,err))
            callback([])
            return
        if family == socket.AF_UNSPEC:
            tmp = ret
            if self.settings["prefer_ipv6"]:
                ret = [ addr for addr in tmp if addr[0] == socket.AF_INET6 ]
                ret += [ addr for addr in tmp if addr[0] == socket.AF_INET ]
            else:
                ret = [ addr for addr in tmp if addr[0] == socket.AF_INET ]
                ret += [ addr for addr in tmp if addr[0] == socket.AF_INET6 ]
        callback([(addr[0], addr[4][0]) for addr in ret])