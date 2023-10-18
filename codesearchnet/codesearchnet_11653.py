def _loadConfig(self):
        ''' load the configuration information from the target hierarchy '''
        config_dicts = [self.additional_config, self.app_config] + [t.getConfig() for t in self.hierarchy]
        # create an identical set of dictionaries, but with the names of the
        # sources in place of the values. When these are merged they will show
        # where each merged property came from:
        config_blame = [
            _mirrorStructure(self.additional_config, 'command-line config'),
            _mirrorStructure(self.app_config, 'application\'s config.json'),
        ] + [
            _mirrorStructure(t.getConfig(), t.getName()) for t in self.hierarchy
        ]

        self.config = _mergeDictionaries(*config_dicts)
        self.config_blame = _mergeDictionaries(*config_blame)