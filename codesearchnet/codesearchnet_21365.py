def write_targets(self):
        """
            write_targets will write the contents of ips and ldap_strings to the targets_file.
        """
        if len(self.ldap_strings) == 0 and len(self.ips) == 0:
            print_notification("No targets left")
            if self.auto_exit:
                if self.notifier:
                    self.notifier.stop()
                self.terminate_processes()

        with open(self.targets_file, 'w') as f:
            f.write('\n'.join(self.ldap_strings + self.ips))