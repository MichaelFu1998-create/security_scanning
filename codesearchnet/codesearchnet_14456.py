def _merge_defaults(self, config):
        """The config object loads its values from two sources, with the
        following precedence:

            1. data/default_config.yaml
            2. The config file itself, passed in to this object in the
               constructor as `path`.

        in case of conflict, the config file dominates.
        """
        fn = resource_filename('osprey', join('data', 'default_config.yaml'))
        with open(fn) as f:
            default = parse(f)
        return reduce(dict_merge, [default, config])