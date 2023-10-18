def load_overrides(path=None):
    """
    Load config overrides from the yml file at |path|, or from default paths. If a path
    is provided and it does not exist, raise an exception

    Default paths: ./mcore.yml, ./.mcore.yml, ./manticore.yml, ./.manticore.yml.
    """

    if path is not None:
        names = [path]
    else:
        possible_names = ['mcore.yml', 'manticore.yml']
        names = [os.path.join('.', ''.join(x)) for x in product(['', '.'], possible_names)]

    for name in names:
        try:
            with open(name, 'r') as yml_f:
                logger.info(f'Reading configuration from {name}')
                parse_config(yml_f)
            break
        except FileNotFoundError:
            pass
    else:
        if path is not None:
            raise FileNotFoundError(f"'{path}' not found for config overrides")