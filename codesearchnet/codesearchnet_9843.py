def _get_registry(self, registry_path_or_url):
        '''dict: Return the registry as dict with profiles keyed by id.'''
        if registry_path_or_url.startswith('http'):
            profiles = self._load_json_url(registry_path_or_url)
        else:
            profiles = self._load_json_file(registry_path_or_url)
        try:
            registry = {}
            for profile in profiles:
                registry[profile['id']] = profile
            return registry
        except KeyError as e:
            msg = (
                'Registry at "{path}" has no "id" column.'
            ).format(path=registry_path_or_url)
            six.raise_from(ValueError(msg), e)