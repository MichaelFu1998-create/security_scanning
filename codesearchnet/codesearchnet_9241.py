def _add_to_conf(self, new_conf):
        """Add new configuration to self.conf.

        Adds configuration parameters in new_con to self.conf.
        If they already existed in conf, overwrite them.

        :param new_conf: new configuration, to add
        """

        for section in new_conf:
            if section not in self.conf:
                self.conf[section] = new_conf[section]
            else:
                for param in new_conf[section]:
                    self.conf[section][param] = new_conf[section][param]