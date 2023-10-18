def callback(self, event):
        """
            Function that gets called on each event from pyinotify.
        """
        # IN_CLOSE_WRITE -> 0x00000008
        if event.mask == 0x00000008:
            if event.name.endswith('.json'):
                print_success("Ldapdomaindump file found")
                if event.name in ['domain_groups.json', 'domain_users.json']:
                    if event.name == 'domain_groups.json':
                        self.domain_groups_file = event.pathname
                    if event.name == 'domain_users.json':
                        self.domain_users_file = event.pathname
                    if self.domain_groups_file and self.domain_users_file:
                        print_success("Importing users")
                        subprocess.Popen(['jk-import-domaindump', self.domain_groups_file, self.domain_users_file])
                elif event.name == 'domain_computers.json':
                    print_success("Importing computers")
                    subprocess.Popen(['jk-import-domaindump', event.pathname])

                # Ldap has been dumped, so remove the ldap targets.
                self.ldap_strings = []
                self.write_targets()

            if event.name.endswith('_samhashes.sam'):
                host = event.name.replace('_samhashes.sam', '')
                # TODO import file.
                print_success("Secretsdump file, host ip: {}".format(host))
                subprocess.Popen(['jk-import-secretsdump', event.pathname])

                # Remove this system from this ip list.
                self.ips.remove(host)
                self.write_targets()