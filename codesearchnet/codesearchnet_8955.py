def _get_install_context(self):
        """
        returns the template context for install.sh and uninstall.sh
        """
        config = self.config
        # layer2 VPN list
        l2vpn = []
        for vpn in self.config.get('openvpn', []):
            if vpn.get('dev_type') != 'tap':
                continue
            tap = vpn.copy()
            l2vpn.append(tap)
        # bridge list
        bridges = []
        for interface in self.config.get('interfaces', []):
            if interface['type'] != 'bridge':
                continue
            bridge = interface.copy()
            if bridge.get('addresses'):
                bridge['proto'] = interface['addresses'][0].get('proto')
                bridge['ip'] = interface['addresses'][0].get('address')
            bridges.append(bridge)
        # crontabs present?
        cron = False
        for _file in config.get('files', []):
            path = _file['path']
            if path.startswith('/crontabs') or path.startswith('crontabs'):
                cron = True
                break
        # return context
        return dict(hostname=config['general']['hostname'],  # hostname is required
                    l2vpn=l2vpn,
                    bridges=bridges,
                    radios=config.get('radios', []),  # radios might be empty
                    cron=cron)