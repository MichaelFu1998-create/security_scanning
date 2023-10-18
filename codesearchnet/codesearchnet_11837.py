def update_settings(self, d, role, path='roles/{role}/settings.yaml'):
        """
        Writes a key/value pair to a settings file.
        """
        try:
            import ruamel.yaml
            load_func = ruamel.yaml.round_trip_load
            dump_func = ruamel.yaml.round_trip_dump
        except ImportError:
            print('Warning: ruamel.yaml not available, reverting to yaml package, possible lost of formatting may occur.')
            import yaml
            load_func = yaml.load
            dump_func = yaml.dump
        settings_fn = path.format(role=role)
        data = load_func(open(settings_fn))
        data.update(d)
        settings_str = dump_func(data)
        open(settings_fn, 'w').write(settings_str)