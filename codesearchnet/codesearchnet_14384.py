def write_temple_config(temple_config, template, version):
    """Writes the temple YAML configuration"""
    with open(temple.constants.TEMPLE_CONFIG_FILE, 'w') as temple_config_file:
        versioned_config = {
            **temple_config,
            **{'_version': version, '_template': template},
        }
        yaml.dump(versioned_config, temple_config_file, Dumper=yaml.SafeDumper)