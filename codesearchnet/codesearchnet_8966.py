def __intermediate_dns_servers(self, uci, address):
        """
        determines UCI interface "dns" option
        """
        # allow override
        if 'dns' in uci:
            return uci['dns']
        # ignore if using DHCP or if "proto" is none
        if address['proto'] in ['dhcp', 'dhcpv6', 'none']:
            return None
        dns = self.netjson.get('dns_servers', None)
        if dns:
            return ' '.join(dns)