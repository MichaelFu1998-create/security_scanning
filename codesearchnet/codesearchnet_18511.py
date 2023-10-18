def get():
    """ Only API function for the config module.

    :return: {dict}     loaded validated configuration.
    """
    config = {}
    try:
        config = _load_config()
    except IOError:
        try:
            _create_default_config()
            config = _load_config()
        except IOError as e:
            raise ConfigError(_FILE_CREATION_ERROR.format(e.args[0]))
    except SyntaxError as e:
        raise ConfigError(_JSON_SYNTAX_ERROR.format(e.args[0]))
    except Exception:
        raise ConfigError(_JSON_SYNTAX_ERROR.format('Yaml syntax error..'))

    try:
        _validate(config)
    except KeyError as e:
        raise ConfigError(_MANDATORY_KEY_ERROR.format(e.args[0]))
    except SyntaxError as e:
        raise ConfigError(_INVALID_KEY_ERROR.format(e.args[0]))
    except ValueError as e:
        raise ConfigError(_INVALID_VALUE_ERROR.format(e.args[0]))

    config['projects-path'] = os.path.expanduser(config['projects-path'])
    _complete_config(config)
    return config