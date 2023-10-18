def __intermediate_addresses(self, interface):
        """
        converts NetJSON address to
        UCI intermediate data structure
        """
        address_list = self.get_copy(interface, 'addresses')
        # do not ignore interfaces if they do not contain any address
        if not address_list:
            return [{'proto': 'none'}]
        result = []
        static = {}
        dhcp = []
        for address in address_list:
            family = address.get('family')
            # dhcp
            if address['proto'] == 'dhcp':
                address['proto'] = 'dhcp' if family == 'ipv4' else 'dhcpv6'
                dhcp.append(self.__intermediate_address(address))
                continue
            if 'gateway' in address:
                uci_key = 'gateway' if family == 'ipv4' else 'ip6gw'
                interface[uci_key] = address['gateway']
            # static
            address_key = 'ipaddr' if family == 'ipv4' else 'ip6addr'
            static.setdefault(address_key, [])
            static[address_key].append('{address}/{mask}'.format(**address))
            static.update(self.__intermediate_address(address))
        if static:
            # do not use CIDR notation when using a single ipv4
            # see https://github.com/openwisp/netjsonconfig/issues/54
            if len(static.get('ipaddr', [])) == 1:
                network = ip_interface(six.text_type(static['ipaddr'][0]))
                static['ipaddr'] = str(network.ip)
                static['netmask'] = str(network.netmask)
            # do not use lists when using a single ipv6 address
            # (avoids to change output of existing configuration)
            if len(static.get('ip6addr', [])) == 1:
                static['ip6addr'] = static['ip6addr'][0]
            result.append(static)
        if dhcp:
            result += dhcp
        return result