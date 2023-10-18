def set(self, ip, netmask=None):
        """Set the IP address and the netmask."""
        if isinstance(ip, str) and netmask is None:
            ipnm = ip.split('/')
            if len(ipnm) != 2:
                raise ValueError('set: invalid CIDR: "%s"' % ip)
            ip = ipnm[0]
            netmask = ipnm[1]
        if isinstance(ip, IPv4Address):
            self._ip = ip
        else:
            self._ip = IPv4Address(ip)
        if isinstance(netmask, IPv4NetMask):
            self._nm = netmask
        else:
            self._nm = IPv4NetMask(netmask)
        ipl = int(self._ip)
        nml = int(self._nm)
        base_add = ipl & nml
        self._ip_num = 0xFFFFFFFF - 1 - nml
        # NOTE: quite a mess.
        #      This's here to handle /32 (-1) and /31 (0) netmasks.
        if self._ip_num in (-1, 0):
            if self._ip_num == -1:
                self._ip_num = 1
            else:
                self._ip_num = 2
            self._net_ip = None
            self._bc_ip = None
            self._first_ip_dec = base_add
            self._first_ip = IPv4Address(self._first_ip_dec, notation=IP_DEC)
            if self._ip_num == 1:
                last_ip_dec = self._first_ip_dec
            else:
                last_ip_dec = self._first_ip_dec + 1
            self._last_ip = IPv4Address(last_ip_dec, notation=IP_DEC)
            return
        self._net_ip = IPv4Address(base_add, notation=IP_DEC)
        self._bc_ip = IPv4Address(base_add + self._ip_num + 1, notation=IP_DEC)
        self._first_ip_dec = base_add + 1
        self._first_ip = IPv4Address(self._first_ip_dec, notation=IP_DEC)
        self._last_ip = IPv4Address(base_add + self._ip_num, notation=IP_DEC)