def __intermediate_interface(self, interface, uci_name):
        """
        converts NetJSON interface to
        UCI intermediate data structure
        """
        interface.update({
            '.type': 'interface',
            '.name': uci_name,
            'ifname': interface.pop('name')
        })
        if 'network' in interface:
            del interface['network']
        if 'mac' in interface:
            # mac address of wireless interface must
            # be set in /etc/config/wireless, therfore
            # we can skip this in /etc/config/network
            if interface.get('type') != 'wireless':
                interface['macaddr'] = interface['mac']
            del interface['mac']
        if 'autostart' in interface:
            interface['auto'] = interface['autostart']
            del interface['autostart']
        if 'disabled' in interface:
            interface['enabled'] = not interface['disabled']
            del interface['disabled']
        if 'wireless' in interface:
            del interface['wireless']
        if 'addresses' in interface:
            del interface['addresses']
        return interface