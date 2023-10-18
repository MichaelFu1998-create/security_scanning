def update_configs(self, config):
        """
        Gather configuration requirements of all plugins
        """
        for what in self.plugins:  # backend, repo etc.
            for key in self.plugins[what]: # s3, filesystem etc.
                # print("Updating configuration of", what, key)
                self.plugins[what][key].config(what='set', params=config)
        return