def dump_config_file(filename, args, parser=None):
    """Dump args to config file."""
    config = ConfigParser()
    config.add_section(SECTION)
    if parser is None:
        for attr in args:
            config.set(SECTION, attr, args.attr)
    else:
        keys_empty_values_not_pass = (
            '--extra-settings', '--languages', '--requirements', '--template', '--timezone')

        # positionals._option_string_actions
        for action in parser._actions:
            if action.dest in ('help', 'config_file', 'config_dump', 'project_name'):
                continue

            keyp = action.option_strings[0]
            option_name = keyp.lstrip('-')
            option_value = getattr(args, action.dest)
            if any([i for i in keys_empty_values_not_pass if i in action.option_strings]):
                if action.dest == 'languages':
                    if len(option_value) == 1 and option_value[0] == 'en':
                        config.set(SECTION, option_name, '')
                    else:
                        config.set(SECTION, option_name, ','.join(option_value))
                else:
                    config.set(SECTION, option_name, option_value if option_value else '')
            elif action.choices == ('yes', 'no'):
                config.set(SECTION, option_name, 'yes' if option_value else 'no')
            elif action.dest == 'templates':
                config.set(SECTION, option_name, option_value if option_value else 'no')
            elif action.dest == 'cms_version':
                version = ('stable' if option_value == CMS_VERSION_MATRIX['stable']
                           else option_value)
                config.set(SECTION, option_name, version)
            elif action.dest == 'django_version':
                version = ('stable' if option_value == DJANGO_VERSION_MATRIX['stable']
                           else option_value)
                config.set(SECTION, option_name, version)
            elif action.const:
                config.set(SECTION, option_name, 'true' if option_value else 'false')
            else:
                config.set(SECTION, option_name, str(option_value))
    with open(filename, 'w') as fp:
        config.write(fp)