def __intermediate_dns_search(self, uci, address):
        """
        determines UCI interface "dns_search" option
        """
        # allow override
        if 'dns_search' in uci:
            return uci['dns_search']
        # ignore if "proto" is none
        if address['proto'] == 'none':
            return None
        dns_search = self.netjson.get('dns_search', None)
        if dns_search:
            return ' '.join(dns_search)