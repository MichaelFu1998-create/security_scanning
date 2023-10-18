def _merge_config(self, config, templates):
        """
        Merges config with templates
        """
        if not templates:
            return config
        # type check
        if not isinstance(templates, list):
            raise TypeError('templates argument must be an instance of list')
        # merge templates with main configuration
        result = {}
        config_list = templates + [config]
        for merging in config_list:
            result = merge_config(result, self._load(merging), self.list_identifiers)
        return result