def parse_config(f):
    """
    Load an yml-formatted configuration from file stream |f|

    :param file f: Where to read the config.
    """

    try:
        c = yaml.safe_load(f)
        for section_name, section in c.items():
            group = get_group(section_name)

            for key, val in section.items():
                group.update(key)
                setattr(group, key, val)
    # Any exception here should trigger the warning; from not being able to parse yaml
    # to reading poorly formatted values
    except Exception:
        raise ConfigError("Failed reading config file. Do you have a local [.]manticore.yml file?")