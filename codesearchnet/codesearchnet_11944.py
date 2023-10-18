def conf_path(self):
        """
        Retrieves the path to the MySQL configuration file.
        """
        from burlap.system import distrib_id, distrib_release
        hostname = self.current_hostname
        if hostname not in self._conf_cache:
            self.env.conf_specifics[hostname] = self.env.conf_default
            d_id = distrib_id()
            d_release = distrib_release()
            for key in ((d_id, d_release), (d_id,)):
                if key in self.env.conf_specifics:
                    self._conf_cache[hostname] = self.env.conf_specifics[key]
        return self._conf_cache[hostname]