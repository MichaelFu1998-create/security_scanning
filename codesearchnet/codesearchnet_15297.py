def get_module_config_cls(module_name: str) -> Type[_AbstractModuleConfig]:  # noqa: D202
    """Build a module configuration class."""

    class ModuleConfig(_AbstractModuleConfig):
        NAME = f'bio2bel:{module_name}'
        FILES = DEFAULT_CONFIG_PATHS + [
            os.path.join(DEFAULT_CONFIG_DIRECTORY, module_name, 'config.ini')
        ]

    return ModuleConfig