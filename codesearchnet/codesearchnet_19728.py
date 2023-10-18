def is_valid_ip(self, ip):
        """Return true if the given address in amongst the usable addresses,
        or if the given CIDR is contained in this one."""
        if not isinstance(ip, (IPv4Address, CIDR)):
            if str(ip).find('/') == -1:
                ip = IPv4Address(ip)
            else:
                # Support for CIDR strings/objects, an idea of Nicola Novello.
                ip = CIDR(ip)
        if isinstance(ip, IPv4Address):
            if ip < self._first_ip or ip > self._last_ip:
                return False
        elif isinstance(ip, CIDR):
            # NOTE: manage /31 networks; 127.0.0.1/31 is considered to
            #       be included in 127.0.0.1/8.
            if ip._nm._ip_dec == 0xFFFFFFFE \
                    and self._nm._ip_dec != 0xFFFFFFFE:
                compare_to_first = self._net_ip._ip_dec
                compare_to_last = self._bc_ip._ip_dec
            else:
                compare_to_first = self._first_ip._ip_dec
                compare_to_last = self._last_ip._ip_dec
            if ip._first_ip._ip_dec < compare_to_first or \
                    ip._last_ip._ip_dec > compare_to_last:
                return False
        return True