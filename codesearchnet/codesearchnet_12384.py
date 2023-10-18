def write_config(config, app_dir, filename='configuration.json'):
    """Write configuration to the applicaiton directory."""
    path = os.path.join(app_dir, filename)
    with open(path, 'w') as f:
        json.dump(
            config, f, indent=4, cls=DetectMissingEncoder,
            separators=(',', ': '))