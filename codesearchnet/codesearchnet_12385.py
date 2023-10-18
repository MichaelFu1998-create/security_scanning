def get_config_module(config_pathname):
    """Imports the config file to yoconfigurator.configs.<config_basename>."""
    configs_mod = 'yoconfigurator.configs'
    if configs_mod not in sys.modules:
        sys.modules[configs_mod] = types.ModuleType(configs_mod)
    module_name = os.path.basename(config_pathname).rsplit('.', 1)[0]
    module_name = configs_mod + '.' + module_name
    return _load_module(module_name, config_pathname)