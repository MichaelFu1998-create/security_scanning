def load_targets(self):
        """
            load_targets will load the services with smb signing disabled and if ldap is enabled the services with the ldap port open.
        """
        ldap_services = []
        if self.ldap:
            ldap_services = self.search.get_services(ports=[389], up=True)

        self.ldap_strings = ["ldap://{}".format(service.address) for service in ldap_services]
        self.services = self.search.get_services(tags=['smb_signing_disabled'])
        self.ips = [str(service.address) for service in self.services]