def get_all_floating_ips(self):
        """
            This function returns a list of FloatingIP objects.
        """
        data = self.get_data("floating_ips")
        floating_ips = list()
        for jsoned in data['floating_ips']:
            floating_ip = FloatingIP(**jsoned)
            floating_ip.token = self.token
            floating_ips.append(floating_ip)
        return floating_ips