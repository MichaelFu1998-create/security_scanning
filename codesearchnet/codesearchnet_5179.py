def get_all_firewalls(self):
        """
            This function returns a list of Firewall objects.
        """
        data = self.get_data("firewalls")
        firewalls = list()
        for jsoned in data['firewalls']:
            firewall = Firewall(**jsoned)
            firewall.token = self.token
            in_rules = list()
            for rule in jsoned['inbound_rules']:
                in_rules.append(InboundRule(**rule))
            firewall.inbound_rules = in_rules
            out_rules = list()
            for rule in jsoned['outbound_rules']:
                out_rules.append(OutboundRule(**rule))
            firewall.outbound_rules = out_rules
            firewalls.append(firewall)
        return firewalls